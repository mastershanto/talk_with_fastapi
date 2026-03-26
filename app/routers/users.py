"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.modules.users.api.router`.
"""

from app.modules.users.api.router import router

<<<<<<< HEAD
All database errors escalate as AppException subclasses, caught by the
global exception handler registered in main.py — no try/except noise here.
"""
from fastapi import APIRouter, status

from app.repositories import user_crud
from app.dependencies import DBSession, Pagination
from app.exceptions import NotFoundException
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithItemsResponse
from app.response_formatter import success_response, list_response

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    summary="List all users",
)
def list_users(db: DBSession, pagination: Pagination) -> dict:
    """Return a paginated list of users (no properties embedded)."""
    users = user_crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)
    user_list = [UserResponse.model_validate(u) for u in users]
    return list_response(user_list, message="Users fetched successfully", code=200)


@router.get(
    "/{user_id}",
    summary="Get a user with their properties",
)
def get_user(user_id: int, db: DBSession) -> dict:
    """Return a single user including the list of properties they own, or 404."""
    user = user_crud.get(db, user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found.")
    user_data = UserWithItemsResponse.model_validate(user)
    return success_response(user_data, message="User fetched successfully", code=200)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(payload: UserCreate, db: DBSession) -> dict:
    """Create and return a new user."""
    user_data = UserResponse.model_validate(user_crud.create(db, obj_in=payload))
    return success_response(user_data, message="User created successfully", code=201)


@router.put(
    "/{user_id}",
    summary="Update a user",
)
def update_user(user_id: int, payload: UserUpdate, db: DBSession) -> dict:
    """
    Partially update a user.

    Only the fields present in the request body are updated
    (uses `exclude_unset=True` inside CRUDBase.update).
    """
    db_user = user_crud.get(db, user_id)
    if not db_user:
        raise NotFoundException(f"User {user_id} not found.")
    user_data = UserResponse.model_validate(user_crud.update(db, db_obj=db_user, obj_in=payload))
    return success_response(user_data, message="User updated successfully", code=200)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
)
def delete_user(user_id: int, db: DBSession) -> dict:
    """
    Hard-delete a user by ID.

    All properties owned by this user are also deleted (CASCADE defined on the
    FK relationship in the Property model).
    """
    db_user = user_crud.get(db, user_id)
    if not db_user:
        raise NotFoundException(f"User {user_id} not found.")
    user_crud.remove(db, record_id=user_id)
    return success_response(data={"id": user_id}, message="User deleted successfully", code=200)
=======
__all__ = ["router"]
>>>>>>> 7199041aea298502b86585a00da5e2a710d75cd3
