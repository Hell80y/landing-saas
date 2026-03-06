from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from apps.api.database import get_session
from apps.api.models import Landing
from apps.api.schemas import (
    ActionResponse,
    GenerateLandingResponse,
    LandingCreate,
    LandingRead,
    LandingUpdate,
    PublishLandingResponse,
)
from apps.api.services.landing_service import get_landing_or_404, touch_updated_at

router = APIRouter(prefix="/api/v1/landings", tags=["landings"])


@router.post("", response_model=LandingRead, status_code=status.HTTP_201_CREATED)
def create_landing(payload: LandingCreate, session: Session = Depends(get_session)) -> Landing:
    landing = Landing(**payload.model_dump())
    session.add(landing)
    session.commit()
    session.refresh(landing)
    return landing


@router.get("/{id}", response_model=LandingRead)
def get_landing(id: UUID, session: Session = Depends(get_session)) -> Landing:
    return get_landing_or_404(session, id)


@router.put("/{id}", response_model=LandingRead)
def update_landing(id: UUID, payload: LandingUpdate, session: Session = Depends(get_session)) -> Landing:
    landing = get_landing_or_404(session, id)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(landing, field, value)
    touch_updated_at(landing)
    session.add(landing)
    session.commit()
    session.refresh(landing)
    return landing


@router.delete("/{id}", response_model=ActionResponse)
def delete_landing(id: UUID, session: Session = Depends(get_session)) -> ActionResponse:
    landing = get_landing_or_404(session, id)
    session.delete(landing)
    session.commit()
    return ActionResponse(message="Landing deleted")


@router.post("/{id}/generate", response_model=GenerateLandingResponse)
def generate_landing(id: UUID, session: Session = Depends(get_session)) -> GenerateLandingResponse:
    landing = get_landing_or_404(session, id)
    if not landing.combined_spec:
        landing.combined_spec = {
            "meta": {"generated": True},
            "design": {},
            "content": {"headline": landing.title},
            "page": {"blocks": ["Hero", "Benefits", "SocialProof", "Pricing", "FAQ", "FinalCTA"]},
            "commerce": {},
            "tracking": {},
        }
    landing.status = "generated"
    touch_updated_at(landing)
    session.add(landing)
    session.commit()
    session.refresh(landing)
    return GenerateLandingResponse(id=landing.id, status=landing.status, combined_spec=landing.combined_spec)


@router.post("/{id}/publish", response_model=PublishLandingResponse)
def publish_landing(id: UUID, session: Session = Depends(get_session)) -> PublishLandingResponse:
    landing = get_landing_or_404(session, id)
    landing.status = "published"
    landing.published_url = f"https://l.example.com/{landing.id}"
    touch_updated_at(landing)
    session.add(landing)
    session.commit()
    session.refresh(landing)
    return PublishLandingResponse(id=landing.id, status=landing.status, published_url=landing.published_url)
