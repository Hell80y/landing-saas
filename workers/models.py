from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import JSON, Boolean, DateTime, Enum as SqlEnum, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class LandingVersionStage(str, Enum):
    COPY_GENERATED = "copy_generated"
    COMBINED_ASSEMBLED = "combined_assembled"
    PUBLISHED = "published"


class LandingVersion(Base):
    """
    Stores generated landing specs across worker pipeline stages.

    Idempotency is enforced via a unique key per landing and stage.
    """

    __tablename__ = "landing_versions"
    __table_args__ = (UniqueConstraint("landing_id", "stage", "idempotency_key", name="uq_landing_version_idempotency"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    landing_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    stage: Mapped[LandingVersionStage] = mapped_column(SqlEnum(LandingVersionStage, name="landing_version_stage"), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    version_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    spec: Mapped[dict] = mapped_column(JSON, nullable=False)
    kv_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publish_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class CombinedSpec(BaseModel):
    """CombinedSpec schema from SPEC.md."""

    model_config = ConfigDict(extra="forbid")

    meta: dict = Field(default_factory=dict)
    design: dict = Field(default_factory=dict)
    content: dict = Field(default_factory=dict)
    page: dict = Field(default_factory=dict)
    commerce: dict = Field(default_factory=dict)
    tracking: dict = Field(default_factory=dict)
