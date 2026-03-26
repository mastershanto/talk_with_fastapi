from fastapi import APIRouter
from app.modules.ai_module.data.adapter import DummyInferenceAdapter
from app.modules.ai_module.presentation.schemas import AIRequest, AIResponse

router = APIRouter()

@router.post('/predict', response_model=AIResponse)
def predict(request: AIRequest):
    adapter = DummyInferenceAdapter()
    return AIResponse(output=adapter.predict(request.prompt))
