from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

import pytest

from app.modules.auth.application.service import AuthService
from app.core.exceptions import ConflictException, UnauthorizedException
from app.modules.auth.schemas.auth import ChangePasswordRequest, RegisterRequest, VerifyOtpRequest


@dataclass
class FakeUser:
    id: int
    name: str
    email: str
    password_hash: str
    role: str = "user"
    agree_to_terms: bool = True
    is_premium: bool = False
    email_verified_at: datetime | None = None
    avatar: str | None = None
    gender: str | None = None
    goal: str | None = None
    days_in_week: int | None = None
    time_in_day: str | None = None
    workout_duration: int | None = None
    refer_photo: str | None = None
    target_bmi: float | None = None
    target_body_fat: float | None = None
    target_weight: float | None = None
    height: float | None = None
    weight: float | None = None
    age: float | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class FakeRepo:
    def __init__(self) -> None:
        self.user = FakeUser(id=1, name="U", email="u@example.com", password_hash="hashed")

    def get_user_by_email(self, email: str) -> FakeUser | None:
        return self.user if self.user.email == email else None

    def create_user(self, **_: object) -> FakeUser:
        return self.user

    def reregister_unverified_user(self, **_: object) -> FakeUser:
        return self.user

    def mark_email_verified(self, user: FakeUser) -> FakeUser:
        user.email_verified_at = datetime.now(timezone.utc)
        return user

    def verify_user_credentials(self, email: str, password: str) -> FakeUser | None:
        return self.user if email == self.user.email and password == "ok" else None

    def get_user_by_id(self, user_id: int) -> FakeUser | None:
        return self.user if user_id == self.user.id else None

    def set_password(self, user: FakeUser, *, new_password: str) -> FakeUser:
        user.password_hash = f"hashed:{new_password}"
        return user

    def update_user_fields(self, user_id: int, *, fields: dict[str, object]) -> FakeUser | None:
        if user_id != self.user.id:
            return None
        for k, v in fields.items():
            setattr(self.user, k, v)
        return self.user

    def delete_user(self, user_id: int) -> bool:
        return user_id == self.user.id

    def generate_login_token(self, user: FakeUser) -> str:
        return f"token:{user.id}"

    def generate_password_reset_token(self, user: FakeUser) -> str:
        return f"reset:{user.id}"


class FakeOtp:
    def __init__(self, verify_ok: bool = True) -> None:
        self.verify_ok = verify_ok

    def issue(self, *, email: str, purpose: str) -> str:
        return "123456"

    def verify(self, *, email: str, purpose: str, otp: str) -> bool:
        return self.verify_ok


def test_register_rejects_already_verified_email() -> None:
    repo = FakeRepo()
    repo.user.email_verified_at = datetime.now(timezone.utc)
    service = AuthService(repo=repo, otp=FakeOtp())

    payload = RegisterRequest(
        name="User",
        email="u@example.com",
        password="Secret123",
        confirm_password="Secret123",
        agree_to_terms=True,
    )

    with pytest.raises(ConflictException):
        service.register(payload)


def test_verify_register_otp_rejects_invalid_otp() -> None:
    service = AuthService(repo=FakeRepo(), otp=FakeOtp(verify_ok=False))

    with pytest.raises(UnauthorizedException):
        service.verify_register_otp(VerifyOtpRequest(email="u@example.com", otp="000000"))


def test_change_password_rejects_wrong_current_password() -> None:
    service = AuthService(repo=FakeRepo(), otp=FakeOtp())
    payload = ChangePasswordRequest(
        current_password="wrong12",
        password="NewSecret123",
        password_confirmation="NewSecret123",
    )

    with pytest.raises(UnauthorizedException):
        service.change_password(1, payload, verify_fn=lambda plain, hashed: plain == "ok")
