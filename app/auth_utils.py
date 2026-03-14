"""Authentication utilities.

Includes:
- Password hashing (bcrypt)
- JWT creation/validation

Token types:
- access: used for authenticated API calls
- reset:  used for password reset flow (short-lived)
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Final

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# ── Password hashing ──────────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT token generation ──────────────────────────────────────────────────────

SECRET_KEY: Final[str] = settings.SECRET_KEY
ALGORITHM: Final[str] = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = settings.ACCESS_TOKEN_EXPIRE_MINUTES

RESET_TOKEN_EXPIRE_MINUTES: Final[int] = 15

TOKEN_TYPE_ACCESS: Final[str] = "access"
TOKEN_TYPE_RESET: Final[str] = "reset"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _create_token(
    *,
    claims: dict[str, Any],
    token_type: str,
    expires_delta: timedelta,
) -> str:
    to_encode = claims.copy()
    now = _utcnow()
    to_encode.update(
        {
            "type": token_type,
            "iat": int(now.timestamp()),
            "exp": int((now + expires_delta).timestamp()),
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(claims: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create an access JWT."""
    return _create_token(
        claims=claims,
        token_type=TOKEN_TYPE_ACCESS,
        expires_delta=expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_reset_token(claims: dict[str, Any]) -> str:
    """Create a short-lived password-reset JWT."""
    return _create_token(
        claims=claims,
        token_type=TOKEN_TYPE_RESET,
        expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES),
    )


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Decode a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary of claims if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
