from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_profile():
    profile_id = f"USR{uuid4().hex[:6].upper()}"
    profile_data = {
        "user_id": profile_id,
        "name": "Asha",
        "email": "asha@example.com",
        "phone": "9999999999",
        "address": {
            "city": "Hyderabad",
            "state": "Telangana",
            "country": "India",
        },
    }

    create_response = client.post("/api/profiles", json=profile_data)
    assert create_response.status_code == 200, create_response.text

    get_response = client.get(f"/api/profiles/{profile_id}")
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["user_id"] == profile_id
    assert body["email"] == "asha@example.com"

    delete_response = client.delete(f"/api/profiles/{profile_id}")
    assert delete_response.status_code == 200
