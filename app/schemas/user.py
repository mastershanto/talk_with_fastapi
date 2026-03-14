"""User request / response schemas.

These schemas are used by the legacy `/api/v1/users` CRUD endpoints.
The project now has dedicated auth endpoints under `/api/v1/auth/*`.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.property import PropertyResponse


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Alice"])
    email: EmailStr
    age: float | None = Field(None, gt=0, lt=150, description="Age in years")


class UserCreate(UserBase):
    """Payload for POST /api/v1/users.

    Note: This is separate from `/api/v1/auth/register`.
    """

    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: float | None = Field(None, gt=0, lt=150)


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithItemsResponse(UserResponse):
    properties: list[PropertyResponse] = []
