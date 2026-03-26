from typing import List

from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]

from app.modules.todo_module.data.models import TodoDB
from app.modules.todo_module.domain.entities import Todo
from app.modules.todo_module.domain.repositories import TodoRepository


class SQLAlchemyTodoRepository(TodoRepository):
    def __init__(self, db: Session):
        self.db = db

    def list(self, offset: int = 0, limit: int = 100) -> List[Todo]:
        rows = self.db.query(TodoDB).offset(offset).limit(limit).all()
        return [Todo(id=row.id, title=row.title, description=row.description, completed=row.completed, created_at=row.created_at, updated_at=row.updated_at) for row in rows]

    def get(self, todo_id: int) -> Todo | None:
        row = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if not row:
            return None
        return Todo(id=row.id, title=row.title, description=row.description, completed=row.completed, created_at=row.created_at, updated_at=row.updated_at)

    def create(self, todo: Todo) -> Todo:
        row = TodoDB(title=todo.title, description=todo.description, completed=todo.completed)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return Todo(id=row.id, title=row.title, description=row.description, completed=row.completed, created_at=row.created_at, updated_at=row.updated_at)

    def update(self, todo_id: int, todo: Todo) -> Todo | None:
        row = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if not row:
            return None
        row.title = todo.title
        row.description = todo.description
        row.completed = todo.completed
        self.db.commit()
        self.db.refresh(row)
        return Todo(id=row.id, title=row.title, description=row.description, completed=row.completed, created_at=row.created_at, updated_at=row.updated_at)

    def delete(self, todo_id: int) -> bool:
        row = self.db.query(TodoDB).filter(TodoDB.id == todo_id).first()
        if not row:
            return False
        self.db.delete(row)
        self.db.commit()
        return True
