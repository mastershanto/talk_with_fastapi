from __future__ import annotations

import secrets

from fastapi.testclient import TestClient

from app.main import app


def test_favorites_flow_smoke() -> None:
    api = "/api/v1"
    email = f"fav_{secrets.token_hex(4)}@example.com"
    password = "TestPass123!"

    with TestClient(app) as client:
        # Register
        r = client.post(
            f"{api}/auth/register",
            json={
                "name": "Fav User",
                "email": email,
                "password": password,
                "confirm_password": password,
                "agree_to_terms": True,
            },
        )
        assert r.status_code == 200
        otp = r.json()["data"]["otp"]

        # Verify OTP -> token + user_id
        r = client.post(f"{api}/auth/register/otp-verify", json={"email": email, "otp": otp})
        assert r.status_code == 200
        token = r.json()["data"]["access_token"]
        user_id = r.json()["data"]["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create property
        r = client.post(
            f"{api}/properties/",
            json={
                "title": "Fav House",
                "description": "desc",
                "price": 12345,
                "location": "Dhaka",
                "property_type": "house",
                "status": "available",
                "area_sqft": 1200,
                "owner_id": user_id,
            },
        )
        assert r.status_code == 201
        prop_id = r.json()["data"]["id"]

        # Add favorite
        r = client.post(f"{api}/favorites/{prop_id}", headers=headers)
        assert r.status_code == 200

        # List favorites
        r = client.get(f"{api}/favorites/", headers=headers)
        assert r.status_code == 200
        assert len(r.json()["data"]) == 1

        # Remove favorite
        r = client.delete(f"{api}/favorites/{prop_id}", headers=headers)
        assert r.status_code == 200

        # List favorites empty
        r = client.get(f"{api}/favorites/", headers=headers)
        assert r.status_code == 200
        assert r.json()["data"] == []
