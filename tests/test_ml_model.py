from fastapi.testclient import TestClient

from app.main import app


def test_ml_predict() -> None:
    with TestClient(app) as client:
        resp = client.post("/ml/predict", json={"features": [0.1, 0.5, 0.9]})
        assert resp.status_code == 200
        data = resp.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 3


def test_ml_predict_empty() -> None:
    with TestClient(app) as client:
        resp = client.post("/ml/predict", json={"features": []})
        assert resp.status_code == 400
