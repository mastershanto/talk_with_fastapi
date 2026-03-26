from typing import List

from app.modules.ml_model.data.model import ModelStore


class PredictionService:
    def __init__(self, model_store: ModelStore):
        self.model_store = model_store

    def predict(self, features: List[float]) -> List[float]:
        return self.model_store.forecast(features)
