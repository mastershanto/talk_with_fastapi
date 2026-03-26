"""Authentication repository.

Encapsulates user authentication operations:
- lookup by email
- credential verification
- user creation for registration
- password updates
- token issuance
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models.user import User
from app.core.auth_utils import hash_password, verify_password, create_access_token, create_reset_token


class AuthRepository:
    """Handles authentication operations like login and user verification."""

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        """Get user by email address."""
        stmt = select(User).where(User.email == email.strip().lower())
        return db.scalar(stmt)

    def verify_user_credentials(self, db: Session, email: str, password: str) -> User | None:
        """
        Verify user credentials (email and password).

        Returns the user if credentials are valid, None otherwise.
        """
        user = self.get_user_by_email(db, email)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def create_user(
        self,
        db: Session,
        *,
        email: str,
        password: str,
        name: str,
        **kwargs
    ) -> User:
        """Create a new user with hashed password."""
        password_hash = hash_password(password)

        user = User(
            email=email.strip().lower(),
            password_hash=password_hash,
            name=name,
            **kwargs
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def mark_email_verified(self, db: Session, user: User) -> User:
        """Set email_verified_at if not already set."""
        if user.email_verified_at is None:
            user.email_verified_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
        return user

    def set_password(self, db: Session, user: User, *, new_password: str) -> User:
        """Update user password hash."""
        user.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return user

    def generate_login_token(self, user: User) -> str:
        """Generate JWT access token for user."""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
        return create_access_token(token_data)

    def generate_password_reset_token(self, user: User) -> str:
        """Generate a short-lived JWT token for password reset."""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "purpose": "password_reset",
        }
        return create_reset_token(token_data)


# Module-level singleton
auth_repo = AuthRepository()
