from datetime import datetime
from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime
