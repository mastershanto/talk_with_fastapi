"""SQLAlchemy implementation of Properties ports."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.properties.ports import PropertyRepository, PropertyRecord
from app.repositories.property import property_crud
from app.schemas.property import PropertyCreate, PropertyUpdate


class SqlAlchemyPropertyRepository(PropertyRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, *, skip: int, limit: int) -> list[PropertyRecord]:
        return property_crud.get_multi(self._db, skip=skip, limit=limit)

    def get(self, property_id: int) -> PropertyRecord | None:
        return property_crud.get(self._db, property_id)

    def create(self, *, payload: PropertyCreate) -> PropertyRecord:
        return property_crud.create(self._db, obj_in=payload)

    def update(self, property_id: int, *, payload: PropertyUpdate) -> PropertyRecord | None:
        db_prop = property_crud.get(self._db, property_id)
        if not db_prop:
            return None
        return property_crud.update(self._db, db_obj=db_prop, obj_in=payload)

    def delete(self, property_id: int) -> bool:
        db_prop = property_crud.get(self._db, property_id)
        if not db_prop:
            return False
        property_crud.remove(self._db, record_id=property_id)
        return True
