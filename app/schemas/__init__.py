"""
Schemas package — re-exports every public schema in one place.

Usage:
    from app.schemas import UserCreate, ItemResponse, MessageResponse
"""
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.item import ItemBase, ItemCreate, ItemUpdate, ItemResponse
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWithItemsResponse,
)

__all__ = [
    # common
    "MessageResponse",
    "PaginatedResponse",
    # item
    "ItemBase",
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
    # user
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserWithItemsResponse",
]
