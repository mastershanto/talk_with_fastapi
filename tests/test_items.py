"""
Integration tests for User and Item endpoints.

Test database
-------------
A temporary SQLite file (`test.db`) is used so the tests are fully
self-contained and do not touch the production / Docker PostgreSQL.

The DATABASE_URL env-var is set BEFORE any app imports so pydantic-settings
picks it up on first load.
"""
import os
import pathlib
from typing import Any

import pytest
from fastapi.testclient import TestClient

# ── Point at SQLite BEFORE importing the application ──────────────────────────
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

_TEST_DB = pathlib.Path("./test.db")
if _TEST_DB.exists():
    _TEST_DB.unlink(missing_ok=True)

from app.main import app  # noqa: E402  (must come after env-var override)

# ── Constants ──────────────────────────────────────────────────────────────────
USERS_URL = "/api/v1/users"
ITEMS_URL = "/api/v1/items"


# ── Session fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def client():
    """
    Session-scoped TestClient that triggers the application lifespan
    (startup creates tables, seeds data; shutdown logs the end).
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def sample_user(client: TestClient) -> dict[str, Any]:
    """Create a user once for the entire test session."""
    resp = client.post(USERS_URL + "/", json={"name": "tester", "age": 30})
    assert resp.status_code == 201, f"User creation failed: {resp.text}"
    return resp.json()


@pytest.fixture(scope="session")
def sample_item(client: TestClient, sample_user: dict[str, Any]) -> dict[str, Any]:
    """Create an item once for the entire test session."""
    payload: dict[str, Any] = {
        "title": "Sample Item",
        "description": "A test item",
        "price": 9.99,
        "is_active": True,
        "owner_id": sample_user["id"],
    }
    resp = client.post(ITEMS_URL + "/", json=payload)
    assert resp.status_code == 201, f"Item creation failed: {resp.text}"
    return resp.json()


# ── User tests ─────────────────────────────────────────────────────────────────

class TestUserEndpoints:
    def test_create_user(self, sample_user: dict) -> None:
        assert sample_user["name"] == "tester"
        assert sample_user["age"] == 30
        assert "id" in sample_user
        assert "created_at" in sample_user
        assert "updated_at" in sample_user

    def test_get_user_with_items(self, client: TestClient, sample_user: dict) -> None:
        resp = client.get(f"{USERS_URL}/{sample_user['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == sample_user["id"]
        assert "items" in data  # UserWithItemsResponse

    def test_list_users(self, client: TestClient, sample_user: dict) -> None:
        resp = client.get(USERS_URL + "/")
        assert resp.status_code == 200
        assert any(u["id"] == sample_user["id"] for u in resp.json())

    def test_update_user(self, client: TestClient, sample_user: dict) -> None:
        resp = client.put(f"{USERS_URL}/{sample_user['id']}", json={"age": 31})
        assert resp.status_code == 200
        assert resp.json()["age"] == 31

    def test_get_nonexistent_user(self, client: TestClient) -> None:
        resp = client.get(f"{USERS_URL}/999999")
        assert resp.status_code == 404

    def test_update_nonexistent_user(self, client: TestClient) -> None:
        resp = client.put(f"{USERS_URL}/999999", json={"age": 25})
        assert resp.status_code == 404

    def test_delete_nonexistent_user(self, client: TestClient) -> None:
        resp = client.delete(f"{USERS_URL}/999999")
        assert resp.status_code == 404


# ── Item tests ─────────────────────────────────────────────────────────────────

class TestItemEndpoints:
    def test_create_item(self, sample_item: dict) -> None:
        assert sample_item["title"] == "Sample Item"
        assert sample_item["price"] == 9.99
        assert "id" in sample_item
        assert "created_at" in sample_item

    def test_get_item(self, client: TestClient, sample_item: dict) -> None:
        resp = client.get(f"{ITEMS_URL}/{sample_item['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == sample_item["id"]

    def test_list_items(self, client: TestClient, sample_item: dict) -> None:
        resp = client.get(ITEMS_URL + "/")
        assert resp.status_code == 200
        assert any(i["id"] == sample_item["id"] for i in resp.json())

    def test_update_item(self, client: TestClient, sample_item: dict) -> None:
        resp = client.put(
            f"{ITEMS_URL}/{sample_item['id']}",
            json={"price": 19.99, "is_active": False},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["price"] == 19.99
        assert data["is_active"] is False

    def test_create_item_invalid_owner(self, client: TestClient) -> None:
        resp = client.post(
            ITEMS_URL + "/",
            json={"title": "Ghost", "price": 1.0, "is_active": True, "owner_id": 999999},
        )
        assert resp.status_code == 400

    def test_get_nonexistent_item(self, client: TestClient) -> None:
        resp = client.get(f"{ITEMS_URL}/999999")
        assert resp.status_code == 404

    def test_delete_item(self, client: TestClient, sample_item: dict) -> None:
        resp = client.delete(f"{ITEMS_URL}/{sample_item['id']}")
        assert resp.status_code == 204

    def test_deleted_item_gone(self, client: TestClient, sample_item: dict) -> None:
        resp = client.get(f"{ITEMS_URL}/{sample_item['id']}")
        assert resp.status_code == 404

    def test_delete_nonexistent_item(self, client: TestClient) -> None:
        resp = client.delete(f"{ITEMS_URL}/999999")
        assert resp.status_code == 404


# ── Health tests ───────────────────────────────────────────────────────────────

class TestHealthEndpoints:
    def test_root(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert "version" in body
        assert "docs" in body

    def test_health(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_health_db(self, client: TestClient) -> None:
        resp = client.get("/health/db")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"
        assert "db_version" in resp.json()
