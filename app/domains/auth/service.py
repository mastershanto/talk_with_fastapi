"""Auth application service (use-cases)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app.auth_utils import decode_token, TOKEN_TYPE_RESET
from app.domains.auth.ports import AuthRepository, OtpService, UserRecord
from app.exceptions import ConflictException, NotFoundException, UnauthorizedException, BadRequestException
from app.otp_service import OTP_PURPOSE_FORGOT_PASSWORD, OTP_PURPOSE_REGISTER
from app.schemas.auth import (
    ChangePasswordRequest,
    EmailOnlyRequest,
    LoginData,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    ResetTokenData,
    UserResponse,
    VerifyOtpRequest,
)


@dataclass(frozen=True)
class RegisterResult:
    email: str
    otp: str


class AuthService:
    def __init__(self, repo: AuthRepository, otp: OtpService) -> None:
        self._repo = repo
        self._otp = otp

    def register(self, payload: RegisterRequest) -> RegisterResult:
        email = payload.email.strip().lower()
        existing = self._repo.get_user_by_email(email)

        if existing and getattr(existing, "email_verified_at", None) is not None:
            raise ConflictException("Email already registered")

        if existing and getattr(existing, "email_verified_at", None) is None:
            user = self._repo.reregister_unverified_user(email=email, name=payload.name, password=payload.password)
        else:
            user = self._repo.create_user(
                email=email,
                password=payload.password,
                name=payload.name,
                role="user",
                agree_to_terms=payload.agree_to_terms,
                is_premium=False,
            )

        otp_code = self._otp.issue(email=email, purpose=OTP_PURPOSE_REGISTER)
        return RegisterResult(email=getattr(user, "email", email), otp=otp_code)

    def resend_register_otp(self, payload: EmailOnlyRequest) -> str:
        email = payload.email.strip().lower()
        user = self._repo.get_user_by_email(email)
        if not user:
            raise NotFoundException("User not found")
        if getattr(user, "email_verified_at", None) is not None:
            raise BadRequestException("Email already verified")
        return self._otp.issue(email=email, purpose=OTP_PURPOSE_REGISTER)

    def verify_register_otp(self, payload: VerifyOtpRequest) -> LoginData:
        email = payload.email.strip().lower()
        user = self._repo.get_user_by_email(email)
        if not user:
            raise NotFoundException("User not found")

        ok = self._otp.verify(email=email, purpose=OTP_PURPOSE_REGISTER, otp=payload.otp)
        if not ok:
            raise UnauthorizedException("Invalid or expired OTP")

        user = self._repo.mark_email_verified(user)
        access_token = self._repo.generate_login_token(user)
        return LoginData(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

    def login(self, payload: LoginRequest) -> LoginData:
        user = self._repo.verify_user_credentials(str(payload.email), payload.password)
        if not user:
            raise UnauthorizedException("Invalid email or password")
        if getattr(user, "email_verified_at", None) is None:
            raise UnauthorizedException("Email is not verified")

        access_token = self._repo.generate_login_token(user)
        return LoginData(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

    def forgot_password(self, payload: EmailOnlyRequest) -> tuple[str, str | None]:
        email = payload.email.strip().lower()
        user = self._repo.get_user_by_email(email)
        otp_code = None
        if user:
            otp_code = self._otp.issue(email=email, purpose=OTP_PURPOSE_FORGOT_PASSWORD)
        return email, otp_code

    def forgot_password_verify(self, payload: VerifyOtpRequest) -> ResetTokenData:
        email = payload.email.strip().lower()
        user = self._repo.get_user_by_email(email)
        if not user:
            raise UnauthorizedException("Invalid or expired OTP")

        ok = self._otp.verify(email=email, purpose=OTP_PURPOSE_FORGOT_PASSWORD, otp=payload.otp)
        if not ok:
            raise UnauthorizedException("Invalid or expired OTP")

        reset_token = self._repo.generate_password_reset_token(user)
        return ResetTokenData(reset_token=reset_token, token_type="bearer")

    def reset_password(self, payload: ResetPasswordRequest) -> LoginData:
        token_payload = decode_token(payload.reset_token)
        if not token_payload or token_payload.get("type") != TOKEN_TYPE_RESET:
            raise UnauthorizedException("Invalid or expired reset token")

        sub = token_payload.get("sub")
        if not sub:
            raise UnauthorizedException("Invalid reset token")

        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            raise UnauthorizedException("Invalid reset token")

        user = self._repo.get_user_by_id(user_id)
        if not user:
            raise UnauthorizedException("Invalid reset token")

        self._repo.set_password(user, new_password=payload.new_password)

        access_token = self._repo.generate_login_token(user)
        return LoginData(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

    def change_password(
        self,
        user_id: int,
        payload: ChangePasswordRequest,
        *,
        verify_fn: Callable[[str, str], bool],
    ) -> UserRecord:
        user = self._repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        password_hash = getattr(user, "password_hash", None)
        if not password_hash or not verify_fn(payload.current_password, password_hash):
            raise UnauthorizedException("Current password is incorrect")

        return self._repo.set_password(user, new_password=payload.password)

    def update_profile(self, user_id: int, *, fields: dict[str, object]) -> UserRecord:
        updated = self._repo.update_user_fields(user_id, fields=fields)
        if not updated:
            raise NotFoundException("User not found")
        return updated

    def delete_account(self, user_id: int) -> str:
        user = self._repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        email = getattr(user, "email", "")
        ok = self._repo.delete_user(user_id)
        if not ok:
            raise NotFoundException("User not found")
        return email
