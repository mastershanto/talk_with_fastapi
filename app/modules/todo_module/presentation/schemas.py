from datetime import datetime

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TodoOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

