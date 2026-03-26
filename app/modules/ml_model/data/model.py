import os
from typing import List

import numpy as np
from app.modules.ml_model.domain.interfaces import InferenceModel

try:
    import joblib
except ImportError:
    joblib = None

try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    import torch
except ImportError:
    torch = None


class DummyClassifier(InferenceModel):
    def predict(self, features: List[float]) -> List[float]:
        if not features:
            raise ValueError("No features supplied")

        threshold = float(np.mean(features))
        return [1.0 if x > threshold else 0.0 for x in features]


class ModelStore:
    def __init__(self):
        self.model: InferenceModel | None = None
        self.model_type: str | None = None

    def load(self, path: str | None = None) -> None:
        if path and os.path.exists(path):
            lower = path.lower()
            if lower.endswith(".pkl") or lower.endswith(".joblib"):
                if joblib is None:
                    raise RuntimeError("joblib is required for loading pickled models")
                self.model = joblib.load(path)
                self.model_type = "joblib"
                return
            if lower.endswith(".h5") or lower.endswith(".keras") or lower.endswith(".pt"):
                if lower.endswith(".h5") or lower.endswith(".keras"):
                    if tf is None:
                        raise RuntimeError("tensorflow is required for loading Keras models")
                    self.model = tf.keras.models.load_model(path)
                    self.model_type = "tensorflow"
                    return
                if lower.endswith(".pt"):
                    if torch is None:
                        raise RuntimeError("torch is required for loading PyTorch models")
                    self.model = torch.load(path)
                    self.model.eval()
                    self.model_type = "pytorch"
                    return

        # fallback
        self.model = DummyClassifier()
        self.model_type = "dummy"

    def forecast(self, features: List[float]) -> List[float]:
        if self.model is None:
            raise RuntimeError("Model not loaded")

        if self.model_type == "tensorflow":
            inputs = np.array([features], dtype=np.float32)
            predictions = self.model.predict(inputs)
            return list(predictions.ravel())

        if self.model_type == "pytorch":
            if torch is None:
                raise RuntimeError("torch dependency missing")
            self.model.eval()
            tensor = torch.tensor([features], dtype=torch.float32)
            with torch.no_grad():
                outputs = self.model(tensor)
            return outputs.detach().numpy().ravel().tolist()

        if self.model_type == "joblib" and hasattr(self.model, "predict"):
            return self.model.predict([features]).tolist()

        if hasattr(self.model, "predict"):
            return self.model.predict(features)

        raise RuntimeError("Loaded model does not support prediction")