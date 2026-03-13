"""
Generic / shared schema components.

These are re-usable across every domain (users, items, etc.).
"""
from typing import Generic, TypeVar

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
