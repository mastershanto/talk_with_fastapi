"""
User request / response schemas.

Hierarchy
---------
UserBase                — shared validation rules
  UserCreate            — POST /users  body
  UserUpdate            — PUT  /users/{id}  body (all fields optional)
  UserResponse          — serialised user (no items)
  UserWithItemsResponse — serialised user including their owned items
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.property import PropertyResponse


class UserBase(BaseModel):
    """Fields shared by all user schemas."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Alice"],
    )
    age: int = Field(
        ...,
        gt=0,
        lt=150,
        examples=[25],
        description="Age in years (must be 1-149)",
    )


class UserCreate(UserBase):
    """Payload for POST /api/v1/users."""

    pass


class UserUpdate(BaseModel):
    """
    Payload for PUT /api/v1/users/{id}.

    All fields are optional — only provided fields are updated.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, gt=0, lt=150)


class UserResponse(UserBase):
    """Serialised user — no items included (use UserWithItemsResponse when needed)."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithItemsResponse(UserResponse):
    """Serialised user including the list of properties they own."""

    properties: list[PropertyResponse] = []
