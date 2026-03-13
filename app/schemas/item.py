"""
Item request / response schemas.

Hierarchy
---------
ItemBase          — shared validation rules
  ItemCreate      — POST /items  body
  ItemUpdate      — PUT  /items/{id}  body (all fields optional)
  ItemResponse    — serialised item returned to the client
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """Fields shared by all item schemas."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["Laptop"],
    )
    description: str | None = Field(
        None,
        max_length=1000,
        examples=["A powerful laptop"],
    )
    price: float = Field(..., ge=0, examples=[999.99])
    is_active: bool = Field(True, description="Whether the item is available")
    owner_id: int = Field(..., gt=0, description="ID of the owning user")


class ItemCreate(ItemBase):
    """Payload for POST /api/v1/items."""

    pass


class ItemUpdate(BaseModel):
    """
    Payload for PUT /api/v1/items/{id}.

    All fields are optional — only provided fields are updated.
    Note: `owner_id` is intentionally excluded (items cannot change ownership).
    """

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: float | None = Field(None, ge=0)
    is_active: bool | None = None


class ItemResponse(ItemBase):
    """Serialised item returned to API consumers."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
