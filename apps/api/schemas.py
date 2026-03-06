from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class LandingCreate(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=150)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=500)
    combined_spec: dict[str, Any] = Field(default_factory=dict)


class LandingUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    combined_spec: dict[str, Any] | None = None


class LandingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: str
    name: str
    title: str
    description: str
    combined_spec: dict[str, Any]
    status: str
    published_url: str | None
    created_at: datetime
    updated_at: datetime


class ActionResponse(BaseModel):
    message: str


class GenerateLandingResponse(BaseModel):
    id: UUID
    status: str
    combined_spec: dict[str, Any]


class PublishLandingResponse(BaseModel):
    id: UUID
    status: str
    published_url: HttpUrl


class StripeOnboardRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    user_id: str = Field(min_length=1, max_length=100)
    refresh_url: HttpUrl
    return_url: HttpUrl


class StripeOnboardResponse(BaseModel):
    account_id: str
    onboarding_url: HttpUrl


class StripeStatusResponse(BaseModel):
    account_id: str
    onboarding_complete: bool
    charges_enabled: bool
    payouts_enabled: bool


class CheckoutSessionRequest(BaseModel):
    landing_id: UUID
    tenant_id: str = Field(min_length=1, max_length=100)
    price_id: str = Field(min_length=1, max_length=100)
    success_url: HttpUrl
    cancel_url: HttpUrl
    customer_email: EmailStr


class CheckoutSessionResponse(BaseModel):
    session_id: str
    checkout_url: HttpUrl
