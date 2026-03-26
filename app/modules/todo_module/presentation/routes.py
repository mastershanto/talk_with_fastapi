from fastapi import APIRouter

from app.modules.todo_module.presentation.schemas import TodoCreate

router = APIRouter()

@router.post('/')
def create_todo(todo: TodoCreate):
    return todo
