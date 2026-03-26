from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.todo.presentation.schemas import TodoCreate, TodoUpdate
from app.modules.todo.domain.entities import TodoItem


class TodoRepository(ABC):
    @abstractmethod
    async def list(self) -> List[TodoItem]:
        ...

    @abstractmethod
    async def get(self, todo_id: int) -> Optional[TodoItem]:
        ...

    @abstractmethod
    async def create(self, todo_create: TodoCreate) -> TodoItem:
        ...

    @abstractmethod
    async def update(self, todo_id: int, todo_update: TodoUpdate) -> Optional[TodoItem]:
        ...

    @abstractmethod
    async def delete(self, todo_id: int) -> bool:
        ...
