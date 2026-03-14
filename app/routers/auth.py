"""Authentication router.

Endpoints implemented:
- Register + email OTP verification
- Login (email + password)
- Forgot password (OTP) + reset password
- Profile (Bearer JWT)

Email delivery for OTP is currently logged for local development.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from fastapi import APIRouter

from app.dependencies import DBSession
from app.exceptions import ConflictException, NotFoundException, UnauthorizedException, BadRequestException
from app.models.user import User
from app.otp_service import (
    OTP_PURPOSE_FORGOT_PASSWORD,
    OTP_PURPOSE_REGISTER,
    issue_otp,
    verify_otp,
)
from app.repositories.auth import auth_repo
from app.schemas.auth import (
    EmailOnlyRequest,
    LoginData,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    ResetTokenData,
    UserResponse,
    VerifyOtpRequest,
)
from app.security import CurrentUser
from app.auth_utils import decode_token, TOKEN_TYPE_RESET


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: DBSession) -> dict:
    """Create an unverified user and send a registration OTP."""
    email = payload.email.strip().lower()
    existing = auth_repo.get_user_by_email(db, email)

    if existing and existing.email_verified_at is not None:
        raise ConflictException("Email already registered")

    if existing and existing.email_verified_at is None:
        # Allow re-registering to re-issue OTP and update profile/password.
        existing.name = payload.name
        auth_repo.set_password(db, existing, new_password=payload.password)
        db.commit()
        db.refresh(existing)
        user = existing
    else:
        user = auth_repo.create_user(
            db,
            email=email,
            password=payload.password,
            name=payload.name,
            role="user",
            agree_to_terms=payload.agree_to_terms,
            is_premium=False,
        )

    otp = issue_otp(db, email=email, purpose=OTP_PURPOSE_REGISTER)

    return {
        "success": True,
        "message": "OTP sent to your email",
        "data": {"email": user.email, "otp": otp},
        "code": 200,
    }


@router.post("/register/resend-otp")
def register_resend_otp(payload: EmailOnlyRequest, db: DBSession) -> dict:
    """Resend registration OTP to an unverified user."""
    email = payload.email.strip().lower()
    user = auth_repo.get_user_by_email(db, email)
    if not user:
        raise NotFoundException("User not found")
    if user.email_verified_at is not None:
        raise BadRequestException("Email already verified")

    otp = issue_otp(db, email=email, purpose=OTP_PURPOSE_REGISTER)
    return {
        "success": True,
        "message": "OTP resent successfully",
        "data": {"email": email, "otp": otp},
        "code": 200,
    }


@router.post("/register/otp-verify")
def register_verify_otp(payload: VerifyOtpRequest, db: DBSession) -> dict:
    """Verify registration OTP, mark user email verified, and return access token."""
    email = payload.email.strip().lower()
    user = auth_repo.get_user_by_email(db, email)
    if not user:
        raise NotFoundException("User not found")

    ok = verify_otp(db, email=email, purpose=OTP_PURPOSE_REGISTER, otp=payload.otp)
    if not ok:
        raise UnauthorizedException("Invalid or expired OTP")

    auth_repo.mark_email_verified(db, user)
    db.refresh(user)

    access_token = auth_repo.generate_login_token(user)
    login_data = LoginData(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

    return {
        "success": True,
        "message": "OTP verified successfully",
        "data": login_data.model_dump(),
        "code": 200,
    }


@router.post("/login")
def login(payload: LoginRequest, db: DBSession) -> dict:
    """Login with email + password and return access token and user payload."""
    user = auth_repo.verify_user_credentials(db, payload.email, payload.password)
    if not user:
        raise UnauthorizedException("Invalid email or password")

    if user.email_verified_at is None:
        raise UnauthorizedException("Email is not verified")

    access_token = auth_repo.generate_login_token(user)
    login_data = LoginData(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

    return {
        "success": True,
        "message": "Login successful",
        "data": login_data.model_dump(),
        "code": 200,
    }


@router.post("/forgot-password")
def forgot_password(payload: EmailOnlyRequest, db: DBSession) -> dict:
    """Send OTP to email for password reset (does not reveal account existence)."""
    email = payload.email.strip().lower()
    user = auth_repo.get_user_by_email(db, email)
    otp = None
    if user:
        otp = issue_otp(db, email=email, purpose=OTP_PURPOSE_FORGOT_PASSWORD)

    data = {"email": email}
    if otp:
        data["otp"] = otp
    return {
        "success": True,
        "message": "If the account exists, an OTP has been sent to the email",
        "data": data,
        "code": 200,
    }


@router.post("/forgot-password/resend-otp")
def forgot_password_resend(payload: EmailOnlyRequest, db: DBSession) -> dict:
    """Resend OTP for password reset (does not reveal account existence)."""
    email = payload.email.strip().lower()
    user = auth_repo.get_user_by_email(db, email)
    otp = None
    if user:
        otp = issue_otp(db, email=email, purpose=OTP_PURPOSE_FORGOT_PASSWORD)
    data = {"email": email}
    if otp:
        data["otp"] = otp
    return {
        "success": True,
        "message": "If the account exists, an OTP has been sent to the email",
        "data": data,
        "code": 200,
    }


@router.post("/forgot-password/otp-verify")
def forgot_password_verify(payload: VerifyOtpRequest, db: DBSession) -> dict:
    """Verify OTP and return a short-lived reset token."""
    email = payload.email.strip().lower()
    user = auth_repo.get_user_by_email(db, email)
    if not user:
        # Avoid revealing; still treat as invalid.
        raise UnauthorizedException("Invalid or expired OTP")

    ok = verify_otp(db, email=email, purpose=OTP_PURPOSE_FORGOT_PASSWORD, otp=payload.otp)
    if not ok:
        raise UnauthorizedException("Invalid or expired OTP")

    reset_token = auth_repo.generate_password_reset_token(user)
    return {
        "success": True,
        "message": "OTP verified successfully",
        "data": ResetTokenData(reset_token=reset_token, token_type="bearer").model_dump(),
        "code": 200,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: DBSession) -> dict:
    """Reset password using the reset_token obtained from OTP verification."""
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

    user = db.get(User, user_id)
    if not user:
        raise UnauthorizedException("Invalid reset token")

    auth_repo.set_password(db, user, new_password=payload.new_password)
    db.refresh(user)

    access_token = auth_repo.generate_login_token(user)
    login_data = LoginData(access_token=access_token, token_type="bearer", user=UserResponse.model_validate(user))

    return {
        "success": True,
        "message": "OTP verified successfully",
        "data": login_data.model_dump(),
        "code": 200,
    }


@router.get("/profile")
def profile(current_user: CurrentUser) -> dict:
    """Return the authenticated user's profile."""
    return {
        "success": True,
        "message": "User data retrieved successfully",
        "data": UserResponse.model_validate(current_user).model_dump(),
        "code": 200,
    }
