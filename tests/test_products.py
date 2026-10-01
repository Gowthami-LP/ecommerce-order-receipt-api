from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_product():
    product_id = f"PROD{uuid4().hex[:6].upper()}"
    product_data = {
        "product_id": product_id,
        "name": "Pixel 9",
        "category": "Mobile",
        "price": 45000,
        "brand": "Google",
        "stock": 12,
    }

    create_response = client.post("/api/products", json=product_data)
    assert create_response.status_code == 200, create_response.text

    get_response = client.get(f"/api/products/{product_id}")
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["product_id"] == product_id
    assert body["brand"] == "Google"

    delete_response = client.delete(f"/api/products/{product_id}")
    assert delete_response.status_code == 200
