from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.todo.domain.repositories import TodoRepository
from app.modules.todo.domain.entities import TodoItem
from app.modules.todo.data.models import TodoORM
from app.modules.todo.presentation.schemas import TodoCreate, TodoUpdate


class TodoRepositoryImpl(TodoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    def _to_dto(self, todo: TodoORM) -> TodoItem:
        return TodoItem(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

    async def list(self) -> List[TodoItem]:
        result = await self.db.execute(select(TodoORM).order_by(TodoORM.id))
        items = result.scalars().all()
        return [self._to_dto(item) for item in items]

    async def get(self, todo_id: int) -> Optional[TodoItem]:
        result = await self.db.execute(select(TodoORM).where(TodoORM.id == todo_id))
        item = result.scalar_one_or_none()
        return self._to_dto(item) if item is not None else None

    async def create(self, todo_create: TodoCreate) -> TodoItem:
        todo = TodoORM(**todo_create.dict())
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return self._to_dto(todo)

    async def update(self, todo_id: int, todo_update: TodoUpdate) -> Optional[TodoItem]:
        stmt = update(TodoORM).where(TodoORM.id == todo_id).values(**{k: v for k, v in todo_update.dict(exclude_none=True).items()})
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get(todo_id)

    async def delete(self, todo_id: int) -> bool:
        stmt = delete(TodoORM).where(TodoORM.id == todo_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0
