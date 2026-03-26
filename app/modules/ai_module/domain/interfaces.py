from abc import ABC, abstractmethod


class AIInferenceAdapter(ABC):
    @abstractmethod
    def predict(self, prompt: str) -> str:
        raise NotImplementedError
