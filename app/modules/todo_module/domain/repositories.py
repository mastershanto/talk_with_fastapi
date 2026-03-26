from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.modules.todo_module.domain.entities import Todo


class TodoRepository(ABC):
    @abstractmethod
    def list(self, offset: int = 0, limit: int = 100) -> List[Todo]:
        raise NotImplementedError

    @abstractmethod
    def get(self, todo_id: int) -> Todo | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, todo: Todo) -> Todo:
        raise NotImplementedError

    @abstractmethod
    def update(self, todo_id: int, todo: Todo) -> Todo | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, todo_id: int) -> bool:
        raise NotImplementedError
