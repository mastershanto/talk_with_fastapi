from fastapi.testclient import TestClient

from app.main import app


def test_todo_crud() -> None:
    with TestClient(app) as client:
        # create
        create_resp = client.post("/todos/", json={"title": "buy milk", "description": "2 liters"})
        assert create_resp.status_code == 201
        todo = create_resp.json()
        assert todo["title"] == "buy milk"
        todo_id = todo["id"]

        # read
        get_resp = client.get(f"/todos/{todo_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == todo_id

        # update
        update_resp = client.put(f"/todos/{todo_id}", json={"completed": True})
        assert update_resp.status_code == 200
        assert update_resp.json()["completed"] is True

        # delete
        delete_resp = client.delete(f"/todos/{todo_id}")
        assert delete_resp.status_code == 204

        # not found afterwards
        assert client.get(f"/todos/{todo_id}").status_code == 404
