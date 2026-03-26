from sqlalchemy.orm import Session

from app.modules.auth_module.data.models import UserDB
from app.modules.auth_module.domain.models import User


class SQLAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        user_db = self.db.query(UserDB).filter(UserDB.username == username).first()
        if not user_db:
            return None
        return User(id=user_db.id, username=user_db.username, email=None, is_active=user_db.is_active)

    def create(self, username: str, email: str, hashed_password: str) -> User:
        user_db = UserDB(username=username, hashed_password=hashed_password)
        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)
        return User(id=user_db.id, username=user_db.username, email=email, is_active=user_db.is_active)
