from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampUUIDMixin


class LandingVersion(TimestampUUIDMixin, Base):
    __tablename__ = "landing_versions"

    landing_id: Mapped[UUID] = mapped_column(ForeignKey("landings.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    combined_spec: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
