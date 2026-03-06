from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampUUIDMixin


class ConnectAccount(TimestampUUIDMixin, Base):
    __tablename__ = "connect_accounts"

    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    stripe_account_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    payouts_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
