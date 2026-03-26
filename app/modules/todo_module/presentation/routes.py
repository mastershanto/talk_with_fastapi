from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db, Base, engine
from app.core.security import get_current_user
from app.modules.todo_module.data.repository import SQLAlchemyTodoRepository
from app.modules.todo_module.services.todo_service import TodoService
from app.modules.todo_module.presentation import schemas

router = APIRouter()

Base.metadata.create_all(bind=engine)


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    repository = SQLAlchemyTodoRepository(db)
    return TodoService(repository)


@router.get('/', response_model=list[schemas.TodoOut])
def list_todos(service: TodoService = Depends(get_todo_service), current_user=Depends(get_current_user)):
    return service.list_todos()


@router.get('/{todo_id}', response_model=schemas.TodoOut)
def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service), current_user=Depends(get_current_user)):
    item = service.get_todo(todo_id)
    if not item:
        raise HTTPException(status_code=404, detail='Todo not found')
    return item


@router.post('/', response_model=schemas.TodoOut, status_code=201)
def create_todo(payload: schemas.TodoCreate, service: TodoService = Depends(get_todo_service), current_user=Depends(get_current_user)):
    return service.create_todo(payload.title, payload.description)


@router.put('/{todo_id}', response_model=schemas.TodoOut)
def update_todo(todo_id: int, payload: schemas.TodoUpdate, service: TodoService = Depends(get_todo_service), current_user=Depends(get_current_user)):
    item = service.update_todo(todo_id, payload.title, payload.description, payload.completed)
    if not item:
        raise HTTPException(status_code=404, detail='Todo not found')
    return item


@router.delete('/{todo_id}', status_code=204)
def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service), current_user=Depends(get_current_user)):
    if not service.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail='Todo not found')
    return None
