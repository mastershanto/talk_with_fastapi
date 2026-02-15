import os

# Use a local SQLite file for tests so the test DB is available at import time
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# ensure a fresh sqlite file so metadata.create_all() creates the correct schema
if os.path.exists("./test.db"):
    try:
        os.remove("./test.db")
    except OSError:
        pass

from typing import Any
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_item_crud_flow():
    # create a user first
    resp = client.post("/users/", json={"name": "tester", "age": 30})
    if resp.status_code != 201:
        print("CREATE USER FAILED:", resp.status_code, resp.text)
    assert resp.status_code == 201
    user = resp.json()
    user_id = user["id"]

    # create an item
    payload: dict[str, Any] = {
        "title": "Sample Item",
        "description": "A test item",
        "price": 9.99,
        "is_active": True,
        "owner_id": user_id,
    }
    resp = client.post("/items/", json=payload)
    if resp.status_code != 201:
        print("CREATE ITEM FAILED:", resp.status_code, resp.text)
    assert resp.status_code == 201, f"CREATE ITEM FAILED: {resp.status_code} {resp.text}"
    item = resp.json()
    assert item["title"] == "Sample Item"
    item_id = item["id"]

    # get the item
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == item_id

    # list items
    resp = client.get("/items/")
    assert resp.status_code == 200
    assert any(i["id"] == item_id for i in resp.json())

    # delete item
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 204

    # ensure item is gone
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404

    # cleanup sqlite file
    try:
        os.remove("./test.db")
    except OSError:
        pass
