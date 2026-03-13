"""Item ORM model."""
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Item(TimestampMixin, Base):
    """
    Represents an item owned by a User.

    Columns
    -------
    id          : surrogate primary key
    title       : short item name (max 200 chars, indexed for search)
    description : optional long text (max 1 000 chars)
    price       : non-negative float price
    is_active   : soft-enable / disable toggle
    owner_id    : FK → users.id (CASCADE DELETE)
    created_at  : UTC timestamp set on insert  (via TimestampMixin)
    updated_at  : UTC timestamp refreshed on update (via TimestampMixin)

    Relationships
    -------------
    owner : many-to-one → User
    """

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    owner: Mapped["User"] = relationship(  # type: ignore[name-defined]
        "User",
        back_populates="items",
    )

    def __repr__(self) -> str:
        return f"<Item id={self.id} title={self.title!r} owner_id={self.owner_id}>"
