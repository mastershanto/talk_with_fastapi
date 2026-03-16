"""
Property/Real Estate model.
"""
from typing import TYPE_CHECKING
from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class PropertyType(str, PyEnum):
    LAND = "land"
    HOUSE = "house"
    APARTMENT = "apartment"
    COMMERCIAL = "commercial"


class PropertyStatus(str, PyEnum):
    AVAILABLE = "available"
    SOLD = "sold"
    PENDING = "pending"


class Property(TimestampMixin, Base):
    """
    Represents a real estate property or land listing.
    """
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Metadata
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType), nullable=False, default=PropertyType.LAND)
    status: Mapped[PropertyStatus] = mapped_column(Enum(PropertyStatus), nullable=False, default=PropertyStatus.AVAILABLE)
    
    # Optional fields for specifics
    area_sqft: Mapped[float] = mapped_column(Float, nullable=True)

    # Owner relationship (keeping User model for owner tracking)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner: Mapped["User"] = relationship("User", back_populates="properties")

    def __repr__(self) -> str:
        return f"<Property id={self.id} title={self.title!r} price={self.price}>"
