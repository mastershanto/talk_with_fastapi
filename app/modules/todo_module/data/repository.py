from typing import List

from app.modules.todo_module.domain.entities import Todo
from app.modules.todo_module.domain.repositories import TodoRepository


class SQLAlchemyTodoRepository(TodoRepository):
    def list(self, offset: int = 0, limit: int = 100) -> List[Todo]:
        raise NotImplementedError

    def get(self, todo_id: int) -> Todo | None:
        raise NotImplementedError

    def create(self, todo: Todo) -> Todo:
        raise NotImplementedError

    def update(self, todo_id: int, todo: Todo) -> Todo | None:
        raise NotImplementedError

    def delete(self, todo_id: int) -> bool:
        raise NotImplementedError
