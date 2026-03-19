"""Iris model adapter (sklearn + joblib)."""
from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from numpy.typing import NDArray
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils._bunch import Bunch


# Resolve model path from project root (4 levels up from this file)
MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "ai_models" / "iris_model.joblib"


class SklearnIrisModel:
    """Simple model wrapper for iris classification."""

    def __init__(self) -> None:
        iris: Bunch = load_iris()  # type: ignore
        self._X: NDArray = iris.data  # type: ignore
        self._y: NDArray = iris.target  # type: ignore
        self._target_names: NDArray = iris.target_names  # type: ignore

        self._model = self._load_or_train()

    def _load_or_train(self) -> RandomForestClassifier:
        if MODEL_PATH.is_file():
            try:
                return joblib.load(MODEL_PATH)
            except Exception:
                pass

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(self._X, self._y)
        try:
            joblib.dump(model, MODEL_PATH)
        except Exception:
            # ignore saving failure in constrained environment
            pass
        return model

    def predict(self, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> str:
        x = [[sepal_length, sepal_width, petal_length, petal_width]]
        label_index = int(self._model.predict(x)[0])
        return str(self._target_names[label_index])
