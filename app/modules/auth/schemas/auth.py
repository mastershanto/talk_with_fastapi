"""Authentication schemas.

This module defines the request/response contracts for the authentication
endpoints. Responses are wrapped using the API contract:

    {
      "success": true,
      "message": "...",
      "data": {...},
      "code": 200
    }
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer


DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    """Standard response envelope used by auth APIs."""

    success: bool
    message: str
    data: DataT
    code: int


# ── Requests ────────────────────────────────────────────────────────────────


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    confirm_password: str = Field(..., min_length=6, max_length=128)
    agree_to_terms: bool = Field(default=False)

    def model_post_init(self, __context: Any) -> None:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class EmailOnlyRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str = Field(..., min_length=6, max_length=128)


class UpdateProfileRequest(BaseModel):
    """Profile update fields (all optional)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    age: float | None = Field(None, gt=0, lt=150)
    height: float | None = Field(None, gt=0)
    weight: float | None = Field(None, gt=0)
    gender: str | None = Field(None, max_length=50)
    goal: str | None = Field(None, max_length=255)
    days_in_week: int | None = Field(None, ge=0, le=7)
    time_in_day: str | None = Field(None, max_length=50)
    workout_duration: int | None = Field(None, ge=0)


class ChangePasswordRequest(BaseModel):
    """Change password request with current password verification."""

    current_password: str = Field(..., min_length=6, max_length=128)
    password: str = Field(..., min_length=6, max_length=128)
    password_confirmation: str = Field(..., min_length=6, max_length=128)

    def model_post_init(self, __context: Any) -> None:
        if self.password != self.password_confirmation:
            raise ValueError("Passwords do not match")


# ── Responses ───────────────────────────────────────────────────────────────


class UserResponse(BaseModel):
    """User payload used by login and profile responses."""

    id: int
    name: str
    email: str
    email_verified_at: datetime | None = None
    role: str
    avatar: str | None = None
    agree_to_terms: bool
    is_premium: bool
    gender: str | None = None
    goal: str | None = None
    days_in_week: int | None = None
    time_in_day: str | None = None
    workout_duration: int | None = None
    refer_photo: str | None = None
    target_bmi: float | None = None
    target_body_fat: float | None = None
    target_weight: float | None = None
    height: float | None = None
    weight: float | None = None
    age: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("agree_to_terms", "is_premium")
    def _bool_as_int(self, value: bool) -> int:
        return 1 if value else 0

    @field_serializer("age", "height", "weight", "target_bmi", "target_body_fat", "target_weight")
    def _float_as_two_decimals(self, value: float | None) -> str | None:
        if value is None:
            return None
        return f"{value:.2f}"


class LoginData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ResetTokenData(BaseModel):
    reset_token: str
    token_type: str = "bearer"


class SimpleData(BaseModel):
    """Minimal data payload for simple success responses."""

    data: dict[str, Any] = {}

