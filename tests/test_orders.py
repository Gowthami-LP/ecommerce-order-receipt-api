from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_order():
    order_id = f"ORD{uuid4().hex[:6].upper()}"
    user_id = f"USR{uuid4().hex[:6].upper()}"
    product_id = f"PROD{uuid4().hex[:6].upper()}"

    client.post(
        "/api/profiles",
        json={
            "user_id": user_id,
            "name": "Asha",
            "email": "asha@example.com",
            "phone": "9999999999",
            "address": {"city": "Hyderabad", "state": "Telangana", "country": "India"},
        },
    )
    client.post(
        "/api/products",
        json={
            "product_id": product_id,
            "name": "Pixel 9",
            "category": "Mobile",
            "price": 45000,
            "brand": "Google",
            "stock": 12,
        },
    )

    order_data = {
        "order_id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "quantity": 2,
        "status": "confirmed",
        "order_date": "2026-09-17",
    }

    create_response = client.post("/api/orders", json=order_data)
    assert create_response.status_code == 200, create_response.text

    get_response = client.get(f"/api/orders/{order_id}")
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["order_id"] == order_id
    assert body["quantity"] == 2

    client.delete(f"/api/orders/{order_id}")
    client.delete(f"/api/products/{product_id}")
    client.delete(f"/api/profiles/{user_id}")
