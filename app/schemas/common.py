"""
Generic / shared schema components.

These are re-usable across every domain (users, items, etc.).
"""
from typing import Generic, TypeVar, Any

from pydantic import BaseModel

DataT = TypeVar("DataT")


class MessageResponse(BaseModel):
    """Generic success/info message returned from write endpoints."""

    message: str


class PaginatedResponse(BaseModel, Generic[DataT]):
    """
    Wrapper for paginated list responses.

    Example response body::

        {
            "items":  [...],
            "total":  42,
            "skip":   0,
            "limit":  20
        }
    """

    items: list[DataT]
    total: int
    skip: int
    limit: int


class ApiResponse(BaseModel, Generic[DataT]):
    """
    Standard API response envelope used across all endpoints.
    
    All API responses must follow this format:
    
    {
        "success": true/false,
        "message": "Human-readable message",
        "data": {...},  # The actual response data
        "code": 200/400/401/etc
    }
    """
    
    success: bool
    message: str
    data: Any  # Use Any to support any type of data
    code: int
