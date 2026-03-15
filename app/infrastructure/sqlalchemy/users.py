"""SQLAlchemy implementation of Users ports."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.users.ports import UserRepository, UserRecord
from app.repositories.user import user_crud
from app.schemas.user import UserCreate, UserUpdate


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, *, skip: int, limit: int) -> list[UserRecord]:
        return user_crud.get_multi(self._db, skip=skip, limit=limit)

    def get(self, user_id: int) -> UserRecord | None:
        return user_crud.get(self._db, user_id)

    def create(self, *, payload: UserCreate) -> UserRecord:
        return user_crud.create(self._db, obj_in=payload)

    def update(self, user_id: int, *, payload: UserUpdate) -> UserRecord | None:
        db_user = user_crud.get(self._db, user_id)
        if not db_user:
            return None
        return user_crud.update(self._db, db_obj=db_user, obj_in=payload)

    def delete(self, user_id: int) -> bool:
        db_user = user_crud.get(self._db, user_id)
        if not db_user:
            return False
        user_crud.remove(self._db, record_id=user_id)
        return True
