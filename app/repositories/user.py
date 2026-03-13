"""
User data-access object.

Extends CRUDBase with user-specific queries.
Import the singleton:  from app.repositories import user_crud
"""
from sqlalchemy.orm import Session

from app.repositories.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations scoped to the User model."""

    def get_by_name(self, db: Session, name: str) -> User | None:
        """Return the first user whose name matches exactly, or None."""
        return (
            db.query(User)
            .filter(User.name == name)
            .first()
        )


# Module-level singleton — import this everywhere.
user_crud = CRUDUser(User)
