"""SQLAlchemy implementation of Auth ports."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_utils import create_access_token, create_reset_token, hash_password, verify_password
from app.modules.auth.ports.ports import AuthRepository, UserRecord
from app.persistence.models.user import User


class SqlAlchemyAuthRepository(AuthRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_user_by_email(self, email: str) -> UserRecord | None:
        stmt = select(User).where(User.email == email.strip().lower())
        return self._db.scalar(stmt)

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
        user = User(
            email=email.strip().lower(),
            password_hash=hash_password(password),
            name=name,
            role=role,
            agree_to_terms=agree_to_terms,
            is_premium=is_premium,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def reregister_unverified_user(self, *, email: str, name: str, password: str) -> UserRecord:
        user = self.get_user_by_email(email)
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
        user.password_hash = hash_password(password)
        self._db.commit()
        self._db.refresh(user)
        return user

    def mark_email_verified(self, user: UserRecord) -> UserRecord:
        if user.email_verified_at is None:
            user.email_verified_at = datetime.now(timezone.utc)
            self._db.commit()
            self._db.refresh(user)
        return user

    def verify_user_credentials(self, email: str, password: str) -> UserRecord | None:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> UserRecord | None:
        return self._db.get(User, user_id)

    def set_password(self, user: UserRecord, *, new_password: str) -> UserRecord:
        user.password_hash = hash_password(new_password)
        self._db.commit()
        self._db.refresh(user)
        return user

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
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
        return create_access_token(token_data)

    def generate_password_reset_token(self, user: UserRecord) -> str:
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "purpose": "password_reset",
        }
        return create_reset_token(token_data)
