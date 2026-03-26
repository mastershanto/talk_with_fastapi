from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.modules.ml_model.data.model import ModelStore
from app.modules.ml_model.presentation.schemas import PredictionRequest, PredictionResponse
from app.modules.ml_model.services.prediction_service import PredictionService

router = APIRouter(prefix="/ml", tags=["ml"])

# Singleton model loader for this example
model_store = ModelStore()
model_store.load(path=settings.ml_model_path)
predictor = PredictionService(model_store)


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    if not request.features:
        raise HTTPException(status_code=400, detail="features cannot be empty")

    predictions = predictor.predict(request.features)
    return PredictionResponse(predictions=predictions)
