"""Schema definitions for iris_talk endpoints."""

from pydantic import BaseModel, Field


class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt=0)
    sepal_width: float = Field(..., gt=0)
    petal_length: float = Field(..., gt=0)
    petal_width: float = Field(..., gt=0)


class PredictionOutput(BaseModel):
    predicted_class: str
