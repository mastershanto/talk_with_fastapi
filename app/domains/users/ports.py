"""Ports (interfaces) for the Users domain.

These are intentionally framework-agnostic: routers depend on services, services
depend on ports, and infrastructure provides concrete implementations.
"""

from __future__ import annotations

from typing import Any, Protocol, Sequence

from app.schemas.user import UserCreate, UserUpdate


UserRecord = Any  # gradually tighten to a domain entity later


class UserRepository(Protocol):
    def list(self, *, skip: int, limit: int) -> Sequence[UserRecord]:
        raise NotImplementedError

    def get(self, user_id: int) -> UserRecord | None:
        raise NotImplementedError

    def create(self, *, payload: UserCreate) -> UserRecord:
        raise NotImplementedError

    def update(self, user_id: int, *, payload: UserUpdate) -> UserRecord | None:
        raise NotImplementedError

    def delete(self, user_id: int) -> bool:
        raise NotImplementedError
