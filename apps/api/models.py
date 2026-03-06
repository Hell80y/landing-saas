from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Landing(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    tenant_id: str = Field(index=True, max_length=100)
    name: str = Field(max_length=150)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=500)
    combined_spec: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False),
    )
    status: str = Field(default="draft", max_length=20)
    published_url: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ConnectAccount(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: str = Field(index=True, max_length=100)
    user_id: str = Field(index=True, max_length=100)
    stripe_account_id: str = Field(unique=True, max_length=100)
    onboarding_complete: bool = Field(default=False)
    charges_enabled: bool = Field(default=False)
    payouts_enabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
