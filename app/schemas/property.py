"""
Property schemas.
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.property import PropertyType, PropertyStatus


class PropertyBase(BaseModel):
    """Shared properties for Property schemas."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    price: float = Field(..., gt=0)
    location: str = Field(..., min_length=1)
    property_type: PropertyType = Field(default=PropertyType.LAND)
    status: PropertyStatus = Field(default=PropertyStatus.AVAILABLE)
    area_sqft: float | None = Field(None, gt=0)


class PropertyCreate(PropertyBase):
    """Payload for creating a property."""
    owner_id: int = Field(..., description="ID of the user who owns this property")


class PropertyUpdate(BaseModel):
    """Payload for updating a property."""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    price: float | None = Field(None, gt=0)
    location: str | None = None
    property_type: PropertyType | None = None
    status: PropertyStatus | None = None
    area_sqft: float | None = Field(None, gt=0)


class PropertyResponse(PropertyBase):
    """Response schema for property."""
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
