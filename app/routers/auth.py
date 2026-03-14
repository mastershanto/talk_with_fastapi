"""Authentication router.

Endpoints implemented:
- Register + email OTP verification
- Login (email + password)
- Forgot password (OTP) + reset password
- Profile (Bearer JWT)

Email delivery for OTP is currently logged for local development.
"""

from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy.orm import Session

from fastapi import APIRouter, File, UploadFile, Form

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
    ChangePasswordRequest,
    EmailOnlyRequest,
    LoginData,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    ResetTokenData,
    UpdateProfileRequest,
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


@router.put("/profile")
def update_profile(
    current_user: CurrentUser,
    db: DBSession,
    name: str | None = Form(None),
    age: float | None = Form(None),
    height: float | None = Form(None),
    weight: float | None = Form(None),
    gender: str | None = Form(None),
    goal: str | None = Form(None),
    days_in_week: int | None = Form(None),
    time_in_day: str | None = Form(None),
    workout_duration: int | None = Form(None),
    refer_photo: UploadFile | None = File(None),
) -> dict:
    """Update the authenticated user's profile with optional file upload."""
    user = db.get(User, current_user.id)
    if not user:
        raise NotFoundException("User not found")

    # Update text fields
    if name is not None:
        user.name = name
    if age is not None:
        user.age = float(age)
    if height is not None:
        user.height = float(height)
    if weight is not None:
        user.weight = float(weight)
    if gender is not None:
        user.gender = gender
    if goal is not None:
        user.goal = goal
    if days_in_week is not None:
        user.days_in_week = int(days_in_week)
    if time_in_day is not None:
        user.time_in_day = time_in_day
    if workout_duration is not None:
        user.workout_duration = int(workout_duration)

    # Handle file upload
    if refer_photo:
        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)

        # Save file with user ID prefix for uniqueness
        if not refer_photo.filename:
            raise BadRequestException("File must have a valid filename")
        
        file_extension = Path(refer_photo.filename).suffix
        safe_filename = f"user_{user.id}_refer_photo{file_extension}"
        file_path = uploads_dir / safe_filename

        # Write file to disk
        contents = refer_photo.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Store filename in database
        user.refer_photo = safe_filename

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": UserResponse.model_validate(user).model_dump(),
        "code": 200,
    }


@router.put("/change-password")
def change_password(current_user: CurrentUser, payload: ChangePasswordRequest, db: DBSession) -> dict:
    """Change the authenticated user's password.
    
    Requires verification of current password.
    """
    user = db.get(User, current_user.id)
    if not user:
        raise NotFoundException("User not found")

    # Verify current password matches
    from app.auth_utils import verify_password
    if not verify_password(payload.current_password, user.password_hash):
        raise UnauthorizedException("Current password is incorrect")

    # Update to new password
    auth_repo.set_password(db, user, new_password=payload.password)
    db.refresh(user)

    return {
        "success": True,
        "message": "Password changed successfully",
        "data": UserResponse.model_validate(user).model_dump(),
        "code": 200,
    }


@router.post("/logout")
def logout(current_user: CurrentUser) -> dict:
    """Logout the authenticated user (client discards JWT token).
    
    Since JWT tokens are stateless, logout simply confirms the action.
    The client should discard the token.
    """
    return {
        "success": True,
        "message": "Logged out successfully",
        "data": {"email": current_user.email},
        "code": 200,
    }


@router.delete("/account")
def delete_account(current_user: CurrentUser, db: DBSession) -> dict:
    """Delete the authenticated user's account permanently."""
    user = db.get(User, current_user.id)
    if not user:
        raise NotFoundException("User not found")

    email = user.email
    
    # Delete uploaded files if any
    if user.refer_photo:
        file_path = Path("uploads") / user.refer_photo
        if file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass  # File deletion failure doesn't block account deletion

    # Delete user from database
    db.delete(user)
    db.commit()

    return {
        "success": True,
        "message": "Account deleted successfully",
        "data": {"email": email},
        "code": 200,
    }
