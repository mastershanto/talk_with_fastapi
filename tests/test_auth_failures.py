from __future__ import annotations

import secrets

from fastapi.testclient import TestClient

from app.main import app


def test_register_verify_with_wrong_otp_returns_unauthorized() -> None:
    api = "/api/v1"
    email = f"wrongotp_{secrets.token_hex(4)}@example.com"
    password = "TestPass123!"

    with TestClient(app) as client:
        r = client.post(
            f"{api}/auth/register",
            json={
                "name": "Wrong OTP User",
                "email": email,
                "password": password,
                "confirm_password": password,
                "agree_to_terms": True,
            },
        )
        assert r.status_code == 200

        r = client.post(
            f"{api}/auth/register/otp-verify",
            json={"email": email, "otp": "000000"},
        )
        assert r.status_code == 401
        body = r.json()
        assert body["success"] is False
        assert "otp" in body["message"].lower()
