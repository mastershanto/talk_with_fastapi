"""
Schemas package — re-exports every public schema in one place.
"""
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.property import PropertyBase, PropertyCreate, PropertyUpdate, PropertyResponse
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
    
    # property
    "PropertyBase",
    "PropertyCreate",
    "PropertyUpdate",
    "PropertyResponse",

    # user
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserWithItemsResponse",
]
