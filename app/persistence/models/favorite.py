"""Property favorites (user ↔ property).

A small, independent model used by the Favorites feature.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class PropertyFavorite(TimestampMixin, Base):
    """A single favorite relation between a user and a property."""

    __tablename__ = "property_favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "property_id", name="uq_property_favorites_user_property"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    property_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
