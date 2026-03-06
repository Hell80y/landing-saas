from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampUUIDMixin


class Event(TimestampUUIDMixin, Base):
    __tablename__ = "events"

    tenant_id: Mapped[UUID | None] = mapped_column(ForeignKey("tenants.id", ondelete="SET NULL"))
    landing_id: Mapped[UUID | None] = mapped_column(ForeignKey("landings.id", ondelete="SET NULL"))
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source: Mapped[str | None] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
