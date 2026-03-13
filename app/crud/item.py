"""
Item data-access object.

Extends CRUDBase with item-specific queries.
Import the singleton:  from app.crud import item_crud
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    """CRUD operations scoped to the Item model."""

    def get_by_owner(
        self,
        db: Session,
        owner_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        """Return paginated items belonging to a specific owner."""
        stmt = (
            select(Item)
            .where(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())


# Module-level singleton — import this everywhere.
item_crud = CRUDItem(Item)
