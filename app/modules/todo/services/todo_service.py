from typing import List, Optional

from app.modules.todo.domain.repositories import TodoRepository
from app.modules.todo.domain.entities import TodoItem
from app.modules.todo.presentation.schemas import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def list_todos(self) -> List[TodoItem]:
        return await self.repository.list()

    async def get_todo(self, todo_id: int) -> Optional[TodoItem]:
        return await self.repository.get(todo_id)

    async def create_todo(self, todo_create: TodoCreate) -> TodoItem:
        return await self.repository.create(todo_create)

    async def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[TodoItem]:
        return await self.repository.update(todo_id, todo_update)

    async def delete_todo(self, todo_id: int) -> bool:
        return await self.repository.delete(todo_id)
