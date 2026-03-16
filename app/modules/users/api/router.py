"""Users HTTP adapter (FastAPI router).

Kept inside the users domain module so the whole feature is co-located:
router + schemas + use-cases + ports.
"""

from fastapi import APIRouter, status

from app.dependencies import Pagination, UserServiceDep
from app.exceptions import NotFoundException
from app.response_formatter import list_response, success_response
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserWithItemsResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    summary="List all users",
)
def list_users(service: UserServiceDep, pagination: Pagination) -> dict:
    users = service.list_users(skip=pagination.skip, limit=pagination.limit)
    user_list = [UserResponse.model_validate(u) for u in users]
    return list_response(user_list, message="Users fetched successfully", code=200)


@router.get(
    "/{user_id}",
    summary="Get a user with their properties",
)
def get_user(user_id: int, service: UserServiceDep) -> dict:
    user = service.get_user(user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found.")
    user_data = UserWithItemsResponse.model_validate(user)
    return success_response(user_data, message="User fetched successfully", code=200)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(payload: UserCreate, service: UserServiceDep) -> dict:
    user_data = UserResponse.model_validate(service.create_user(payload))
    return success_response(user_data, message="User created successfully", code=201)


@router.put(
    "/{user_id}",
    summary="Update a user",
)
def update_user(user_id: int, payload: UserUpdate, service: UserServiceDep) -> dict:
    updated = service.update_user(user_id, payload)
    if not updated:
        raise NotFoundException(f"User {user_id} not found.")
    user_data = UserResponse.model_validate(updated)
    return success_response(user_data, message="User updated successfully", code=200)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
)
def delete_user(user_id: int, service: UserServiceDep) -> dict:
    ok = service.delete_user(user_id)
    if not ok:
        raise NotFoundException(f"User {user_id} not found.")
    return success_response(data={"id": user_id}, message="User deleted successfully", code=200)
