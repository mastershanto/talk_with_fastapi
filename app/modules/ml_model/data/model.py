from typing import List

from app.modules.ml_model.domain.interfaces import InferenceModel


class DummyClassifier(InferenceModel):
    def predict(self, features: List[float]) -> List[float]:
        if not features:
            raise ValueError("No features supplied")

        norm = sum(features) / len(features)
        return [1.0 if x > norm else 0.0 for x in features]


class ModelStore:
    def __init__(self):
        self.model: InferenceModel | None = None

    def load(self) -> None:
        self.model = DummyClassifier()

    def forecast(self, features: List[float]) -> List[float]:
        if self.model is None:
            raise RuntimeError("Model not loaded")
        return self.model.predict(features)
