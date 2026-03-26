from fastapi import HTTPException, status

from app.core.security import create_access_token, decode_access_token, verify_password
from app.modules.auth.data.user_store import get_user
from app.modules.auth.domain.models import User, UserInDB


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_token_for_user(user: UserInDB) -> str:
    to_encode = {"sub": user.username}
    return create_access_token(to_encode)


def get_current_user(token: str) -> User:
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return User(**user.model_dump())
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
