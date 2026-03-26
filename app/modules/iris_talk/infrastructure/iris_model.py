"""Iris model adapter (sklearn + joblib)."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
from numpy.typing import NDArray
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils._bunch import Bunch


# Resolve model path from project root (4 levels up from this file)
MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "ai_models" / "iris_model.joblib"


@lru_cache(maxsize=1)
def _get_cached_model_and_targets() -> tuple[RandomForestClassifier, NDArray]:
    iris: Bunch = load_iris()  # type: ignore
    x: NDArray = iris.data  # type: ignore
    y: NDArray = iris.target  # type: ignore
    target_names: NDArray = iris.target_names  # type: ignore

    if MODEL_PATH.is_file():
        try:
            loaded = joblib.load(MODEL_PATH)
            if isinstance(loaded, RandomForestClassifier):
                return loaded, target_names
        except Exception:
            pass

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x, y)
    try:
        joblib.dump(model, MODEL_PATH)
    except Exception:
        # ignore saving failure in constrained environment
        pass
    return model, target_names


class SklearnIrisModel:
    """Simple model wrapper for iris classification."""

    def __init__(self) -> None:
        self._model, self._target_names = _get_cached_model_and_targets()

    def predict(self, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> str:
        x = np.asarray([[sepal_length, sepal_width, petal_length, petal_width]], dtype=float)
        label_index = int(self._model.predict(x)[0])
        return str(self._target_names[label_index])
