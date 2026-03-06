from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from apps.api.database import get_session
from apps.api.models import ConnectAccount, Landing
from apps.api.schemas import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    StripeOnboardRequest,
    StripeOnboardResponse,
    StripeStatusResponse,
)

router = APIRouter(prefix="/api/v1", tags=["payments"])


@router.post("/stripe/connect/onboard", response_model=StripeOnboardResponse)
def stripe_connect_onboard(
    payload: StripeOnboardRequest,
    session: Session = Depends(get_session),
) -> StripeOnboardResponse:
    statement = select(ConnectAccount).where(
        ConnectAccount.tenant_id == payload.tenant_id,
        ConnectAccount.user_id == payload.user_id,
    )
    account = session.exec(statement).first()

    if not account:
        account = ConnectAccount(
            tenant_id=payload.tenant_id,
            user_id=payload.user_id,
            stripe_account_id=f"acct_{uuid4().hex[:16]}",
        )

    account.updated_at = datetime.now(timezone.utc)
    session.add(account)
    session.commit()
    session.refresh(account)

    onboarding_url = f"https://connect.stripe.com/setup/s/{account.stripe_account_id}"
    return StripeOnboardResponse(account_id=account.stripe_account_id, onboarding_url=onboarding_url)


@router.get("/stripe/connect/status", response_model=StripeStatusResponse)
def stripe_connect_status(
    tenant_id: str = Query(min_length=1),
    user_id: str = Query(min_length=1),
    session: Session = Depends(get_session),
) -> StripeStatusResponse:
    statement = select(ConnectAccount).where(
        ConnectAccount.tenant_id == tenant_id,
        ConnectAccount.user_id == user_id,
    )
    account = session.exec(statement).first()
    if not account:
        raise HTTPException(status_code=404, detail="Connect account not found")

    return StripeStatusResponse(
        account_id=account.stripe_account_id,
        onboarding_complete=account.onboarding_complete,
        charges_enabled=account.charges_enabled,
        payouts_enabled=account.payouts_enabled,
    )


@router.post("/checkout/session", response_model=CheckoutSessionResponse)
def create_checkout_session(
    payload: CheckoutSessionRequest,
    session: Session = Depends(get_session),
) -> CheckoutSessionResponse:
    landing = session.get(Landing, payload.landing_id)
    if not landing or landing.tenant_id != payload.tenant_id:
        raise HTTPException(status_code=404, detail="Landing not found for tenant")

    if landing.status != "published":
        raise HTTPException(status_code=400, detail="Landing must be published before checkout")

    session_id = f"cs_test_{uuid4().hex[:24]}"
    checkout_url = f"https://checkout.stripe.com/pay/{session_id}"
    return CheckoutSessionResponse(session_id=session_id, checkout_url=checkout_url)
