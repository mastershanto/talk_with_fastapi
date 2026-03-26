from pydantic import BaseModel


class AIRequest(BaseModel):
    prompt: str


class AIResponse(BaseModel):
    output: str
