from abc import ABC, abstractmethod
from typing import List


class InferenceModel(ABC):
    @abstractmethod
    def predict(self, features: List[float]) -> List[float]:
        ...
