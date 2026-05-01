from typing import List

from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]

from app.modules.todo_module.data.models import TodoDB
from app.modules.todo_module.data.models import NoteDB
from app.modules.todo_module.domain.entities import Todo
from app.modules.todo_module.domain.entities import Note
from app.modules.todo_module.domain.repositories import TodoRepository
from app.modules.todo_module.domain.repositories import NoteRepository


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


class SQLAlchemyNoteRepository(NoteRepository):
    def __init(self,db):
        self.db=db
    
    def list(self, offset: int=0, limit: int =100)-> List[Note]:
        rows=self.db.query(NoteDB).offset(offset).limit(limit).all()
        return [Note(
            id=row.id, 
            title=row.title,
            description=row.description,
            completed=row.completed,
            created_at=row.created_at,
            updated_at=row.created_at     
        )
         for row in rows]
        
    def get(self, note_id:int)-> Note | None:
        row=self.db.query(NoteDB).filter(NoteDB.id==note_id).first()
        if not row:
            return None
        return Note(id=row.id, title=row.title, description=row.description, completed=row.completed, created_at=row.created_at, updated_at= row.updated_at)
    def create(self, note:Note)-> Note:
        row=NoteDB(title=note.title,description=note.description, completed: note.complted )
        self.db.add(row)
        self.db.commit()
        self.db.refreshe(row)
       
        return Note(id=row.id, title=row.title, description=row.description, completed=row.completed, created_at=row.created_at, updated_at=row.updated_at)
        
    def update (self, todo_id: int, todo: Todo)-> Todo| None:
        row=self.db.query(NoteDB).filter(NoteDB.id==todo_id).first()
        row.title=todo.title
        row.description=todo.description
        row.completed=todo.completed
        
        if not row:
         return None
        
        return Note(id=row.id, title=row.title, description=row.description, completed= row.completed, created_at=row.created_at, updated_at=row.updated_at)
    def delete(self, todo_id:int)-> bool:
        row=self.db.query(NoteDB).filter(NoteDB.id==todo_id).first()
        self.db.delete(row)
        self.db.commit()
        return True
    