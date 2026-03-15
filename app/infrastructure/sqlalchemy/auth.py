"""SQLAlchemy implementation of Auth ports."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.auth.ports import AuthRepository, UserRecord
from app.models.user import User
from app.repositories.auth import auth_repo


class SqlAlchemyAuthRepository(AuthRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_user_by_email(self, email: str) -> UserRecord | None:
        return auth_repo.get_user_by_email(self._db, email)

    def create_user(
        self,
        *,
        email: str,
        password: str,
        name: str,
        role: str,
        agree_to_terms: bool,
        is_premium: bool,
    ) -> UserRecord:
        return auth_repo.create_user(
            self._db,
            email=email,
            password=password,
            name=name,
            role=role,
            agree_to_terms=agree_to_terms,
            is_premium=is_premium,
        )

    def reregister_unverified_user(self, *, email: str, name: str, password: str) -> UserRecord:
        user = auth_repo.get_user_by_email(self._db, email)
        if not user:
            # fall back to create (shouldn't happen in normal flow)
            return self.create_user(
                email=email,
                password=password,
                name=name,
                role="user",
                agree_to_terms=True,
                is_premium=False,
            )

        user.name = name
        auth_repo.set_password(self._db, user, new_password=password)
        self._db.commit()
        self._db.refresh(user)
        return user

    def mark_email_verified(self, user: UserRecord) -> UserRecord:
        return auth_repo.mark_email_verified(self._db, user)

    def verify_user_credentials(self, email: str, password: str) -> UserRecord | None:
        return auth_repo.verify_user_credentials(self._db, email, password)

    def get_user_by_id(self, user_id: int) -> UserRecord | None:
        return self._db.get(User, user_id)

    def set_password(self, user: UserRecord, *, new_password: str) -> UserRecord:
        return auth_repo.set_password(self._db, user, new_password=new_password)

    def update_user_fields(self, user_id: int, *, fields: dict[str, object]) -> UserRecord | None:
        user = self._db.get(User, user_id)
        if not user:
            return None

        for key, value in fields.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self._db.get(User, user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True

    def generate_login_token(self, user: UserRecord) -> str:
        return auth_repo.generate_login_token(user)

    def generate_password_reset_token(self, user: UserRecord) -> str:
        return auth_repo.generate_password_reset_token(user)
