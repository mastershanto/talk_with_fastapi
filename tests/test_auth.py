from fastapi.testclient import TestClient

from app.main import app


def test_auth_token_and_me() -> None:
    with TestClient(app) as client:
        login_resp = client.post("/api/v1/auth/token", json={"username": "alice", "password": "password123"})
        assert login_resp.status_code == 200
        data = login_resp.json()
        assert "access_token" in data

        token = data["access_token"]
        me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_resp.status_code == 200
        me_data = me_resp.json()
        assert me_data["username"] == "alice"
