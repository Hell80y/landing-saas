from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session

from apps.api.models import Landing


def get_landing_or_404(session: Session, landing_id: UUID) -> Landing:
    landing = session.get(Landing, landing_id)
    if not landing:
        raise HTTPException(status_code=404, detail="Landing not found")
    return landing


def touch_updated_at(landing: Landing) -> None:
    landing.updated_at = datetime.now(timezone.utc)
