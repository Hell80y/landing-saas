from fastapi.testclient import TestClient

from apps.api.database import create_db_and_tables
from apps.api.main import app


client = TestClient(app)


def test_landing_crud_and_actions() -> None:
    create_db_and_tables()

    create_response = client.post(
        "/api/v1/landings",
        json={
            "tenant_id": "tenant_1",
            "name": "Demo Landing",
            "title": "Demo Product",
            "description": "Desc",
            "combined_spec": {},
        },
    )
    assert create_response.status_code == 201
    landing = create_response.json()
    landing_id = landing["id"]

    get_response = client.get(f"/api/v1/landings/{landing_id}")
    assert get_response.status_code == 200

    update_response = client.put(
        f"/api/v1/landings/{landing_id}",
        json={"title": "Updated Demo Product"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Demo Product"

    generate_response = client.post(f"/api/v1/landings/{landing_id}/generate")
    assert generate_response.status_code == 200
    assert generate_response.json()["status"] == "generated"

    publish_response = client.post(f"/api/v1/landings/{landing_id}/publish")
    assert publish_response.status_code == 200
    assert publish_response.json()["status"] == "published"

    delete_response = client.delete(f"/api/v1/landings/{landing_id}")
    assert delete_response.status_code == 200


def test_stripe_and_checkout_routes() -> None:
    create_db_and_tables()

    create_landing = client.post(
        "/api/v1/landings",
        json={
            "tenant_id": "tenant_2",
            "name": "Paid Landing",
            "title": "Paid Product",
            "description": "Desc",
            "combined_spec": {},
        },
    )
    landing_id = create_landing.json()["id"]
    client.post(f"/api/v1/landings/{landing_id}/publish")

    onboard_response = client.post(
        "/api/v1/stripe/connect/onboard",
        json={
            "tenant_id": "tenant_2",
            "user_id": "user_2",
            "refresh_url": "https://app.example.com/refresh",
            "return_url": "https://app.example.com/return",
        },
    )
    assert onboard_response.status_code == 200

    status_response = client.get(
        "/api/v1/stripe/connect/status",
        params={"tenant_id": "tenant_2", "user_id": "user_2"},
    )
    assert status_response.status_code == 200

    checkout_response = client.post(
        "/api/v1/checkout/session",
        json={
            "landing_id": landing_id,
            "tenant_id": "tenant_2",
            "price_id": "price_123",
            "success_url": "https://app.example.com/success",
            "cancel_url": "https://app.example.com/cancel",
            "customer_email": "buyer@example.com",
        },
    )
    assert checkout_response.status_code == 200
    assert "checkout_url" in checkout_response.json()
