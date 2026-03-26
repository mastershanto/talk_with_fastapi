"""Iris talk HTTP adapter."""

from fastapi import APIRouter

from app.core.response_formatter import success_response
from app.modules.iris_talk.application.service import IrisTalkService
from app.modules.iris_talk.schemas.iris import IrisInput, PredictionOutput

router = APIRouter(prefix="/iris-talk", tags=["IrisTalk"])

_service = IrisTalkService()


@router.get("/", summary="Iris talk health")
def root() -> dict:
    return success_response(data={"status": "ok"}, message="IrisTalk module is ready", code=200)


@router.post("/predict", summary="Predict Iris class")
def predict(payload: IrisInput) -> dict:
    predicted_class = _service.predict(payload)
    return success_response(
        data={"predicted_class": predicted_class},
        message="Prediction complete",
        code=200,
    )
