from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampUUIDMixin


class Tenant(TimestampUUIDMixin, Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    billing_email: Mapped[str | None] = mapped_column(String(320))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
