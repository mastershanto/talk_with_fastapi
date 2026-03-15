"""SQLAlchemy implementation of Properties ports."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.properties.ports import PropertyRepository, PropertyRecord
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate


class SqlAlchemyPropertyRepository(PropertyRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, *, skip: int, limit: int) -> list[PropertyRecord]:
        stmt = select(Property).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())

    def get(self, property_id: int) -> PropertyRecord | None:
        return self._db.get(Property, property_id)

    def create(self, *, payload: PropertyCreate) -> PropertyRecord:
        data = payload.model_dump()
        db_obj = Property(**data)
        self._db.add(db_obj)
        self._db.commit()
        self._db.refresh(db_obj)
        return db_obj

    def update(self, property_id: int, *, payload: PropertyUpdate) -> PropertyRecord | None:
        db_prop = self._db.get(Property, property_id)
        if not db_prop:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_prop, field, value)

        self._db.commit()
        self._db.refresh(db_prop)
        return db_prop

    def delete(self, property_id: int) -> bool:
        db_prop = self._db.get(Property, property_id)
        if not db_prop:
            return False
        self._db.delete(db_prop)
        self._db.commit()
        return True
