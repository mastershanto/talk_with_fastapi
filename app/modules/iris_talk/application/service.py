"""Application service for Iris prediction use cases."""

import math

from app.core.exceptions import BadRequestException
from app.modules.iris_talk.infrastructure.iris_model import SklearnIrisModel
from app.modules.iris_talk.schemas.iris import IrisInput


class IrisTalkService:
    def __init__(self, model: SklearnIrisModel | None = None) -> None:
        self._model = model or SklearnIrisModel()

    def predict(self, payload: IrisInput) -> str:
        values = [
            float(payload.sepal_length),
            float(payload.sepal_width),
            float(payload.petal_length),
            float(payload.petal_width),
        ]
        if not all(math.isfinite(v) for v in values):
            raise BadRequestException("All feature values must be finite numbers")

        return self._model.predict(
            values[0],
            values[1],
            values[2],
            values[3],
        )
