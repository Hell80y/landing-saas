from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampUUIDMixin


class Landing(TimestampUUIDMixin, Base):
    __tablename__ = "landings"

    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    published_version_id: Mapped[UUID | None] = mapped_column(ForeignKey("landing_versions.id", ondelete="SET NULL"))
    description: Mapped[str | None] = mapped_column(Text)
