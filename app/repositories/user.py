"""User data-access object.

Extends CRUDBase with user-specific queries.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_utils import hash_password
from app.repositories.base import CRUDBase
from app.persistence.models.user import User
from app.modules.users.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations scoped to the User model."""

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email.strip().lower())
        return db.scalar(stmt)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        data = obj_in.model_dump(exclude={"password"})
        data["email"] = str(obj_in.email).strip().lower()
        data["password_hash"] = hash_password(obj_in.password)
        data.setdefault("role", "user")
        data.setdefault("agree_to_terms", True)
        data.setdefault("is_premium", False)

        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name(self, db: Session, name: str) -> User | None:
        """Return the first user whose name matches exactly, or None."""
        return (
            db.query(User)
            .filter(User.name == name)
            .first()
        )


# Module-level singleton — import this everywhere.
user_crud = CRUDUser(User)
