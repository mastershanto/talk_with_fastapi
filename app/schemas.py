"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base user schema"""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., gt=0, lt=150)


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, gt=0, lt=150)


class UserResponse(UserBase):
    """Schema for user response"""
    id: int

    model_config = ConfigDict(from_attributes=True)
