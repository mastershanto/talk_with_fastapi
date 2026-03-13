"""User ORM model."""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class User(TimestampMixin, Base):
    """
    Represents an application user.

    Columns
    -------
    id         : surrogate primary key
    name       : display name (max 100 chars)
    age        : age in years (validated in schema: 1-149)
    created_at : UTC timestamp set on insert (via TimestampMixin)
    updated_at : UTC timestamp refreshed on every update (via TimestampMixin)

    Relationships
    -------------
    items: "properties" : one-to-many → Property  (cascade delete to avoid orphans)
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    properties: Mapped[list["Property"]] = relationship(  # type: ignore[name-defined]
        "Property",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} age={self.age}>"
