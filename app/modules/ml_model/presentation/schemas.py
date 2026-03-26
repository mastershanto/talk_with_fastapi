from typing import List

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    features: List[float]


class PredictionResponse(BaseModel):
    predictions: List[float]
