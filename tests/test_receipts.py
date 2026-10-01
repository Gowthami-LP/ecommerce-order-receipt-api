from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_receipt_endpoint_and_missing_entities():
    user_id = f"USR{uuid4().hex[:6].upper()}"
    product_id = f"PROD{uuid4().hex[:6].upper()}"
    order_id = f"ORD{uuid4().hex[:6].upper()}"
    invoice_id = f"INV{uuid4().hex[:6].upper()}"

    profile_response = client.post(
        "/api/profiles",
        json={
            "user_id": user_id,
            "name": "Bhavana",
            "email": "bhavana@example.com",
            "phone": "8888888888",
            "address": {"city": "Bengaluru", "state": "Karnataka", "country": "India"},
        },
    )
    assert profile_response.status_code == 200

    product_response = client.post(
        "/api/products",
        json={
            "product_id": product_id,
            "name": "AirPods Pro",
            "category": "Accessories",
            "price": 18000,
            "brand": "Apple",
            "stock": 20,
        },
    )
    assert product_response.status_code == 200

    order_response = client.post(
        "/api/orders",
        json={
            "order_id": order_id,
            "user_id": user_id,
            "product_id": product_id,
            "quantity": 1,
            "status": "delivered",
            "order_date": "2026-09-17",
        },
    )
    assert order_response.status_code == 200

    invoice_response = client.post(
        "/api/invoices",
        json={
            "invoice_id": invoice_id,
            "order_id": order_id,
            "subtotal": 18000,
            "tax": 3240,
            "discount": 0,
            "shipping": 0,
            "total": 21240,
            "payment_status": "paid",
        },
    )
    assert invoice_response.status_code == 200

    receipt_response = client.get(f"/api/orders/{order_id}/receipt")
    assert receipt_response.status_code == 200, receipt_response.text
    body = receipt_response.json()
    assert body["order"]["order_id"] == order_id
    assert body["customer"]["user_id"] == user_id
    assert body["product"]["product_id"] == product_id
    assert body["invoice"]["invoice_id"] == invoice_id

    missing_order = client.get("/api/orders/ORD9999/receipt")
    assert missing_order.status_code == 404

    missing_product_order = client.post(
        "/api/orders",
        json={
            "order_id": f"ORD{uuid4().hex[:6].upper()}",
            "user_id": user_id,
            "product_id": "PROD404",
            "quantity": 1,
            "status": "pending",
            "order_date": "2026-09-18",
        },
    )
    assert missing_product_order.status_code == 200
    missing_product = client.get(f"/api/orders/{missing_product_order.json()['order_id']}/receipt")
    assert missing_product.status_code == 404

    invoice_missing_order = client.post(
        "/api/orders",
        json={
            "order_id": f"ORD{uuid4().hex[:6].upper()}",
            "user_id": user_id,
            "product_id": product_id,
            "quantity": 1,
            "status": "pending",
            "order_date": "2026-09-19",
        },
    )
    assert invoice_missing_order.status_code == 200
    missing_invoice = client.get(f"/api/orders/{invoice_missing_order.json()['order_id']}/receipt")
    assert missing_invoice.status_code == 404

    client.delete(f"/api/invoices/{invoice_id}")
    client.delete(f"/api/orders/{order_id}")
    client.delete(f"/api/products/{product_id}")
    client.delete(f"/api/profiles/{user_id}")
