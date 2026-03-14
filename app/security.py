"""Security dependencies (JWT Bearer auth)."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth_utils import decode_token, TOKEN_TYPE_ACCESS
from app.dependencies import get_db
from app.exceptions import UnauthorizedException
from app.models.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    """Return the authenticated user from a Bearer JWT."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Authentication required")

    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != TOKEN_TYPE_ACCESS:
        raise UnauthorizedException("Invalid or expired token")

    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedException("Invalid token")

    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise UnauthorizedException("Invalid token")

    user = db.get(User, user_id)
    if not user:
        raise UnauthorizedException("Invalid token")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
