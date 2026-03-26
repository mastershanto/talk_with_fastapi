from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.todo.data.repository import TodoRepositoryImpl
from app.modules.todo.presentation.schemas import TodoCreate, TodoRead, TodoUpdate
from app.modules.todo.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todo"])


@router.get("/", response_model=list[TodoRead])
async def list_todos(session: AsyncSession = Depends(get_session)) -> list[TodoRead]:
    service = TodoService(TodoRepositoryImpl(session))
    return await service.list_todos()


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_create: TodoCreate, session: AsyncSession = Depends(get_session)) -> TodoRead:
    service = TodoService(TodoRepositoryImpl(session))
    return await service.create_todo(todo_create)


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(todo_id: int, session: AsyncSession = Depends(get_session)) -> TodoRead:
    service = TodoService(TodoRepositoryImpl(session))
    todo = await service.get_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    session: AsyncSession = Depends(get_session),
) -> TodoRead:
    service = TodoService(TodoRepositoryImpl(session))
    todo = await service.update_todo(todo_id, todo_update)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, session: AsyncSession = Depends(get_session)) -> None:
    service = TodoService(TodoRepositoryImpl(session))
    success = await service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return None
