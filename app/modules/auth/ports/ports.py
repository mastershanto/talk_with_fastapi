"""Ports (interfaces) for the Auth domain."""

from __future__ import annotations

from typing import Any, Protocol


UserRecord = Any  # gradually tighten to a domain entity later


class AuthRepository(Protocol):
    def get_user_by_email(self, email: str) -> UserRecord | None:
        raise NotImplementedError

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
        raise NotImplementedError

    def reregister_unverified_user(self, *, email: str, name: str, password: str) -> UserRecord:
        raise NotImplementedError

    def mark_email_verified(self, user: UserRecord) -> UserRecord:
        raise NotImplementedError

    def verify_user_credentials(self, email: str, password: str) -> UserRecord | None:
        raise NotImplementedError

    def get_user_by_id(self, user_id: int) -> UserRecord | None:
        raise NotImplementedError

    def set_password(self, user: UserRecord, *, new_password: str) -> UserRecord:
        raise NotImplementedError

    def update_user_fields(self, user_id: int, *, fields: dict[str, Any]) -> UserRecord | None:
        raise NotImplementedError

    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError

    def generate_login_token(self, user: UserRecord) -> str:
        raise NotImplementedError

    def generate_password_reset_token(self, user: UserRecord) -> str:
        raise NotImplementedError


class OtpService(Protocol):
    def issue(self, *, email: str, purpose: str) -> str:
        raise NotImplementedError

    def verify(self, *, email: str, purpose: str, otp: str) -> bool:
        raise NotImplementedError
