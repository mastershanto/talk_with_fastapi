"""Application service for Iris prediction use cases."""

from app.modules.iris_talk.infrastructure.iris_model import SklearnIrisModel
from app.modules.iris_talk.schemas.iris import IrisInput


class IrisTalkService:
    def __init__(self, model: SklearnIrisModel | None = None) -> None:
        self._model = model or SklearnIrisModel()

    def predict(self, payload: IrisInput) -> str:
        return self._model.predict(
            payload.sepal_length,
            payload.sepal_width,
            payload.petal_length,
            payload.petal_width,
        )
