"""SQLAlchemy implementation of Users ports."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth_utils import hash_password
from app.domains.users.ports import UserRepository, UserRecord
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self, *, skip: int, limit: int) -> list[UserRecord]:
        stmt = select(User).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())

    def get(self, user_id: int) -> UserRecord | None:
        return self._db.get(User, user_id)

    def create(self, *, payload: UserCreate) -> UserRecord:
        data = payload.model_dump(exclude={"password"})
        data["email"] = str(payload.email).strip().lower()
        data["password_hash"] = hash_password(payload.password)
        data.setdefault("role", "user")
        data.setdefault("agree_to_terms", True)
        data.setdefault("is_premium", False)

        db_obj = User(**data)
        self._db.add(db_obj)
        self._db.commit()
        self._db.refresh(db_obj)
        return db_obj

    def update(self, user_id: int, *, payload: UserUpdate) -> UserRecord | None:
        db_user = self._db.get(User, user_id)
        if not db_user:
            return None

        data = payload.model_dump(exclude_unset=True)
        if "email" in data and data["email"] is not None:
            data["email"] = str(data["email"]).strip().lower()

        for field, value in data.items():
            setattr(db_user, field, value)

        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self._db.get(User, user_id)
        if not db_user:
            return False
        self._db.delete(db_user)
        self._db.commit()
        return True
