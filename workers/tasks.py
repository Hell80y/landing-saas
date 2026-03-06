from __future__ import annotations

import hashlib
import json
from typing import Any

import requests
from celery import shared_task
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workers.config import SETTINGS
from workers.db import get_session, init_models
from workers.models import CombinedSpec, LandingVersion, LandingVersionStage


def _stable_hash(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _idempotency_key(request_id: str | None, payload: dict[str, Any]) -> str:
    return request_id or _stable_hash(payload)


def _get_existing_version(
    *,
    landing_id: int,
    stage: LandingVersionStage,
    idempotency_key: str,
) -> LandingVersion | None:
    with get_session() as session:
        stmt = select(LandingVersion).where(
            LandingVersion.landing_id == landing_id,
            LandingVersion.stage == stage,
            LandingVersion.idempotency_key == idempotency_key,
        )
        return session.execute(stmt).scalar_one_or_none()


def _persist_version(
    *,
    landing_id: int,
    stage: LandingVersionStage,
    idempotency_key: str,
    spec: dict[str, Any],
    published: bool = False,
    kv_key: str | None = None,
    publish_ref: str | None = None,
) -> LandingVersion:
    version_hash = _stable_hash(spec)

    with get_session() as session:
        row = LandingVersion(
            landing_id=landing_id,
            stage=stage,
            idempotency_key=idempotency_key,
            version_hash=version_hash,
            spec=spec,
            published=published,
            kv_key=kv_key,
            publish_ref=publish_ref,
        )
        session.add(row)
        try:
            session.flush()
            session.refresh(row)
            return row
        except IntegrityError:
            session.rollback()
            stmt = select(LandingVersion).where(
                LandingVersion.landing_id == landing_id,
                LandingVersion.stage == stage,
                LandingVersion.idempotency_key == idempotency_key,
            )
            existing = session.execute(stmt).scalar_one()
            return existing


def _build_copy(input_payload: dict[str, Any]) -> dict[str, Any]:
    product_name = str(input_payload.get("product_name", "Product")).strip() or "Product"
    audience = str(input_payload.get("audience", "customers")).strip() or "customers"
    tone = str(input_payload.get("tone", "clear")).strip() or "clear"

    return {
        "headline": f"{product_name} for {audience}",
        "subheadline": f"Launch faster with {tone} messaging that converts.",
        "cta": input_payload.get("cta", "Start now"),
        "bullets": input_payload.get(
            "bullets",
            [
                "Fast setup",
                "Conversion-oriented copy blocks",
                "Built for iterative experimentation",
            ],
        ),
    }


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def generate_copy_spec(
    self,
    *,
    landing_id: int,
    input_payload: dict[str, Any],
    request_id: str | None = None,
) -> dict[str, Any]:
    """Generate idempotent copy content and persist in landing_versions."""
    init_models()

    payload = {"landing_id": landing_id, "input_payload": input_payload}
    key = _idempotency_key(request_id, payload)

    existing = _get_existing_version(landing_id=landing_id, stage=LandingVersionStage.COPY_GENERATED, idempotency_key=key)
    if existing:
        return {"landing_id": landing_id, "stage": existing.stage.value, "spec": existing.spec, "version_hash": existing.version_hash}

    copy_spec = _build_copy(input_payload)
    row = _persist_version(
        landing_id=landing_id,
        stage=LandingVersionStage.COPY_GENERATED,
        idempotency_key=key,
        spec=copy_spec,
    )
    return {"landing_id": landing_id, "stage": row.stage.value, "spec": row.spec, "version_hash": row.version_hash}


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def assemble_combined_spec(
    self,
    *,
    landing_id: int,
    copy_spec: dict[str, Any],
    design: dict[str, Any] | None = None,
    page: dict[str, Any] | None = None,
    commerce: dict[str, Any] | None = None,
    tracking: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Build CombinedSpec and persist in landing_versions idempotently."""
    init_models()

    payload = {
        "landing_id": landing_id,
        "copy_spec": copy_spec,
        "design": design or {},
        "page": page or {},
        "commerce": commerce or {},
        "tracking": tracking or {},
        "meta": meta or {},
    }
    key = _idempotency_key(request_id, payload)

    existing = _get_existing_version(landing_id=landing_id, stage=LandingVersionStage.COMBINED_ASSEMBLED, idempotency_key=key)
    if existing:
        return {"landing_id": landing_id, "stage": existing.stage.value, "spec": existing.spec, "version_hash": existing.version_hash}

    combined = CombinedSpec(
        meta=meta or {},
        design=design or {},
        content=copy_spec,
        page=page or {},
        commerce=commerce or {},
        tracking=tracking or {},
    ).model_dump()

    row = _persist_version(
        landing_id=landing_id,
        stage=LandingVersionStage.COMBINED_ASSEMBLED,
        idempotency_key=key,
        spec=combined,
    )
    return {"landing_id": landing_id, "stage": row.stage.value, "spec": row.spec, "version_hash": row.version_hash}


def _publish_spec_to_kv(*, kv_key: str, spec: dict[str, Any]) -> str:
    """Publish spec to external KV sync endpoint when configured."""
    if not SETTINGS.kv_publish_endpoint:
        return "noop://kv-disabled"

    headers = {"Content-Type": "application/json"}
    if SETTINGS.kv_publish_token:
        headers["Authorization"] = f"Bearer {SETTINGS.kv_publish_token}"

    response = requests.post(
        SETTINGS.kv_publish_endpoint,
        json={"key": kv_key, "value": spec},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.text or "published"


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def publish_to_kv(
    self,
    *,
    landing_id: int,
    combined_spec: dict[str, Any],
    kv_key: str | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Idempotently publish CombinedSpec to KV and persist publish version."""
    init_models()

    payload = {"landing_id": landing_id, "combined_spec": combined_spec, "kv_key": kv_key}
    key = _idempotency_key(request_id, payload)
    effective_kv_key = kv_key or f"landing:{landing_id}:combined_spec"

    existing = _get_existing_version(landing_id=landing_id, stage=LandingVersionStage.PUBLISHED, idempotency_key=key)
    if existing:
        return {
            "landing_id": landing_id,
            "stage": existing.stage.value,
            "spec": existing.spec,
            "version_hash": existing.version_hash,
            "kv_key": existing.kv_key,
            "published": existing.published,
            "publish_ref": existing.publish_ref,
        }

    # Validate against CombinedSpec contract from SPEC.md
    validated_spec = CombinedSpec.model_validate(combined_spec).model_dump()
    publish_ref = _publish_spec_to_kv(kv_key=effective_kv_key, spec=validated_spec)

    row = _persist_version(
        landing_id=landing_id,
        stage=LandingVersionStage.PUBLISHED,
        idempotency_key=key,
        spec=validated_spec,
        kv_key=effective_kv_key,
        published=True,
        publish_ref=publish_ref,
    )
    return {
        "landing_id": landing_id,
        "stage": row.stage.value,
        "spec": row.spec,
        "version_hash": row.version_hash,
        "kv_key": row.kv_key,
        "published": row.published,
        "publish_ref": row.publish_ref,
    }
