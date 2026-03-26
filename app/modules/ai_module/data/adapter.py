from app.modules.ai_module.domain.interfaces import AIInferenceAdapter


class DummyInferenceAdapter(AIInferenceAdapter):
    def predict(self, prompt: str) -> str:
        return f'AI: {prompt}'
