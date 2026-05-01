from dataclasses import dataclass
from datetime import datetime


@dataclass
class Todo:
    id: int | None
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

@dataclass
class Note:
    id: int | None
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None= None

