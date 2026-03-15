from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoints() -> None:
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"

        r = client.get("/health/db")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"
