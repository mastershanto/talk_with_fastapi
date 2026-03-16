"""Users application service (use-cases).

Keep orchestration here so FastAPI routers stay thin, and persistence stays
behind a port.
"""

from __future__ import annotations

from app.domains.users.ports import UserRepository, UserRecord
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def list_users(self, *, skip: int, limit: int) -> list[UserRecord]:
        return list(self._repo.list(skip=skip, limit=limit))

    def get_user(self, user_id: int) -> UserRecord | None:
        return self._repo.get(user_id)

    def create_user(self, payload: UserCreate) -> UserRecord:
        return self._repo.create(payload=payload)

    def update_user(self, user_id: int, payload: UserUpdate) -> UserRecord | None:
        return self._repo.update(user_id, payload=payload)

    def delete_user(self, user_id: int) -> bool:
        return self._repo.delete(user_id)
