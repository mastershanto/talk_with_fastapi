"""
Generic CRUD base class — the foundation for every data-access object.

Pattern (repository pattern + generics):

    class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
        def get_by_email(self, db: Session, email: str) -> User | None:
            ...

    user_crud = CRUDUser(User)

Public API
----------
get(db, id)                    → ModelT | None
get_multi(db, skip, limit)     → list[ModelT]
count(db)                      → int
create(db, obj_in)             → ModelT
update(db, db_obj, obj_in)     → ModelT
remove(db, id)                 → ModelT | None
"""
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.database import Base

# Generic type variables
ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class CRUDBase(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    """
    Provides type-safe, reusable create/read/update/delete operations for
    any SQLAlchemy model + matching Pydantic schemas.

    Subclass it to add domain-specific queries on top of the base CRUD.
    """

    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    # ── Read ──────────────────────────────────────────────────────────────────

    def get(self, db: Session, record_id: int) -> ModelT | None:
        """Return a single record by primary key, or None if not found."""
        return db.get(self.model, record_id)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelT]:
        """Return a paginated slice of all records, ordered by insertion."""
        stmt = select(self.model).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def count(self, db: Session) -> int:
        """Return the total number of records in the table."""
        stmt = select(func.count()).select_from(self.model)
        return db.scalar(stmt) or 0

    # ── Write ─────────────────────────────────────────────────────────────────

    def create(self, db: Session, *, obj_in: CreateSchemaT) -> ModelT:
        """
        Persist a new record from a Pydantic create-schema.

        All keys from `obj_in.model_dump()` are passed directly to the
        model constructor, so make sure schema fields match model columns.
        """
        data = obj_in.model_dump()
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelT,
        obj_in: UpdateSchemaT | dict[str, Any],
    ) -> ModelT:
        """
        Apply a partial or full update to an existing record.

        Accepts either a dict or a Pydantic update-schema.
        When a Pydantic schema is given, only fields that were explicitly
        set (not defaulted) are updated (`exclude_unset=True`).
        """
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, record_id: int) -> ModelT | None:
        """
        Delete a record by primary key.

        Returns the deleted object (useful for audit logging), or None if
        the record did not exist.
        """
        db_obj = self.get(db, record_id)
        if db_obj is None:
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj
