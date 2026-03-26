"""User ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.persistence.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.persistence.models.property import Property


class User(TimestampMixin, Base):
    """
    Represents an application user.

    Columns
    -------
    id                    : surrogate primary key
    name                  : display name (max 100 chars)
    email                 : unique email for login
    password_hash         : bcrypt hashed password
    email_verified_at     : timestamp when email was verified
    role                  : user role (admin, user, etc.)
    avatar                : avatar URL or path
    agree_to_terms        : whether user agreed to terms
    is_premium            : whether user is premium member
    age                   : age in years
    gender                : gender (male, female, other)
    height                : height in cm
    weight                : weight in kg
    goal                  : fitness goal
    days_in_week          : days per week for workout
    time_in_day           : time of day for workout
    workout_duration      : duration of workout in minutes
    refer_photo           : reference photo URL
    target_bmi            : target BMI
    target_body_fat       : target body fat percentage
    target_weight         : target weight in kg
    created_at            : UTC timestamp set on insert (via TimestampMixin)
    updated_at            : UTC timestamp refreshed on every update (via TimestampMixin)

    Relationships
    -------------
    items: "properties" : one-to-many → Property  (cascade delete to avoid orphans)
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False)
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agree_to_terms: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(50), nullable=True)
    height: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    days_in_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_in_day: Mapped[str | None] = mapped_column(String(50), nullable=True)
    workout_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    refer_photo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_bmi: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_body_fat: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_weight: Mapped[float | None] = mapped_column(Float, nullable=True)

    properties: Mapped[list[Property]] = relationship(
        "Property",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} email={self.email!r}>"
