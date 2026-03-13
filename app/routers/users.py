"""
User endpoints.

Routes
------
GET    /api/v1/users            list_users    — paginated list
    "/api/v1/users/{id}       get_user      — single user + their properties
POST   /api/v1/users            create_user   — create new user
PUT    /api/v1/users/{id}       update_user   — partial update
DELETE /api/v1/users/{id}       delete_user   — hard delete (cascades to properties)

All database errors escalate as AppException subclasses, caught by the
global exception handler registered in main.py — no try/except noise here.
"""
from fastapi import APIRouter, status

from app.repositories import user_crud
from app.dependencies import DBSession, Pagination
from app.exceptions import NotFoundException
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithItemsResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List all users",
)
def list_users(db: DBSession, pagination: Pagination) -> list[UserResponse]:
    """Return a paginated list of users (no properties embedded)."""
    users = user_crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserWithItemsResponse,
    summary="Get a user with their properties",
)
def get_user(user_id: int, db: DBSession) -> UserWithItemsResponse:
    """Return a single user including the list of properties they own, or 404."""
    user = user_crud.get(db, user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found.")
    return UserWithItemsResponse.model_validate(user)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(payload: UserCreate, db: DBSession) -> UserResponse:
    """Create and return a new user."""
    return UserResponse.model_validate(user_crud.create(db, obj_in=payload))


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
)
def update_user(user_id: int, payload: UserUpdate, db: DBSession) -> UserResponse:
    """
    Partially update a user.

    Only the fields present in the request body are updated
    (uses `exclude_unset=True` inside CRUDBase.update).
    """
    db_user = user_crud.get(db, user_id)
    if not db_user:
        raise NotFoundException(f"User {user_id} not found.")
    return UserResponse.model_validate(user_crud.update(db, db_obj=db_user, obj_in=payload))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
def delete_user(user_id: int, db: DBSession) -> None:
    """
    Hard-delete a user by ID.

    All properties owned by this user are also deleted (CASCADE defined on the
    FK relationship in the Property model).
    """
    db_user = user_crud.get(db, user_id)
    if not db_user:
        raise NotFoundException(f"User {user_id} not found.")
    user_crud.remove(db, record_id=user_id)
