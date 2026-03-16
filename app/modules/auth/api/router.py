"""Auth HTTP adapter (FastAPI router)."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile

from app.core.auth_utils import verify_password
from app.core.dependencies import AuthServiceDep
from app.core.exceptions import BadRequestException
from app.modules.auth.schemas.auth import (
    ChangePasswordRequest,
    EmailOnlyRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    UserResponse,
    VerifyOtpRequest,
)
from app.core.security import CurrentUser


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(payload: RegisterRequest, service: AuthServiceDep) -> dict:
    result = service.register(payload)
    return {
        "success": True,
        "message": "OTP sent to your email",
        "data": {"email": result.email, "otp": result.otp},
        "code": 200,
    }


@router.post("/register/resend-otp")
def register_resend_otp(payload: EmailOnlyRequest, service: AuthServiceDep) -> dict:
    otp = service.resend_register_otp(payload)
    email = payload.email.strip().lower()
    return {
        "success": True,
        "message": "OTP resent successfully",
        "data": {"email": email, "otp": otp},
        "code": 200,
    }


@router.post("/register/otp-verify")
def register_verify_otp(payload: VerifyOtpRequest, service: AuthServiceDep) -> dict:
    login_data = service.verify_register_otp(payload)
    return {
        "success": True,
        "message": "OTP verified successfully",
        "data": login_data.model_dump(),
        "code": 200,
    }


@router.post("/login")
def login(payload: LoginRequest, service: AuthServiceDep) -> dict:
    login_data = service.login(payload)
    return {
        "success": True,
        "message": "Login successful",
        "data": login_data.model_dump(),
        "code": 200,
    }


@router.post("/forgot-password")
def forgot_password(payload: EmailOnlyRequest, service: AuthServiceDep) -> dict:
    email, otp = service.forgot_password(payload)
    data: dict[str, str] = {"email": email}
    if otp:
        data["otp"] = otp
    return {
        "success": True,
        "message": "If the account exists, an OTP has been sent to the email",
        "data": data,
        "code": 200,
    }


@router.post("/forgot-password/resend-otp")
def forgot_password_resend(payload: EmailOnlyRequest, service: AuthServiceDep) -> dict:
    email, otp = service.forgot_password(payload)
    data: dict[str, str] = {"email": email}
    if otp:
        data["otp"] = otp
    return {
        "success": True,
        "message": "If the account exists, an OTP has been sent to the email",
        "data": data,
        "code": 200,
    }


@router.post("/forgot-password/otp-verify")
def forgot_password_verify(payload: VerifyOtpRequest, service: AuthServiceDep) -> dict:
    reset_data = service.forgot_password_verify(payload)
    return {
        "success": True,
        "message": "OTP verified successfully",
        "data": reset_data.model_dump(),
        "code": 200,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, service: AuthServiceDep) -> dict:
    login_data = service.reset_password(payload)
    return {
        "success": True,
        "message": "OTP verified successfully",
        "data": login_data.model_dump(),
        "code": 200,
    }


@router.get("/profile")
def profile(current_user: CurrentUser) -> dict:
    return {
        "success": True,
        "message": "User data retrieved successfully",
        "data": UserResponse.model_validate(current_user).model_dump(),
        "code": 200,
    }


@router.put("/profile")
def update_profile(
    current_user: CurrentUser,
    service: AuthServiceDep,
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
    fields: dict[str, object] = {}
    if name is not None:
        fields["name"] = name
    if age is not None:
        fields["age"] = float(age)
    if height is not None:
        fields["height"] = float(height)
    if weight is not None:
        fields["weight"] = float(weight)
    if gender is not None:
        fields["gender"] = gender
    if goal is not None:
        fields["goal"] = goal
    if days_in_week is not None:
        fields["days_in_week"] = int(days_in_week)
    if time_in_day is not None:
        fields["time_in_day"] = time_in_day
    if workout_duration is not None:
        fields["workout_duration"] = int(workout_duration)

    if refer_photo:
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)

        if not refer_photo.filename:
            raise BadRequestException("File must have a valid filename")

        file_extension = Path(refer_photo.filename).suffix
        safe_filename = f"user_{current_user.id}_refer_photo{file_extension}"
        file_path = uploads_dir / safe_filename

        contents = refer_photo.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        fields["refer_photo"] = safe_filename

    updated_user = service.update_profile(current_user.id, fields=fields)
    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": UserResponse.model_validate(updated_user).model_dump(),
        "code": 200,
    }


@router.put("/change-password")
def change_password(current_user: CurrentUser, payload: ChangePasswordRequest, service: AuthServiceDep) -> dict:
    user = service.change_password(current_user.id, payload, verify_fn=verify_password)
    return {
        "success": True,
        "message": "Password changed successfully",
        "data": UserResponse.model_validate(user).model_dump(),
        "code": 200,
    }


@router.post("/logout")
def logout(current_user: CurrentUser) -> dict:
    return {
        "success": True,
        "message": "Logged out successfully",
        "data": {"email": current_user.email},
        "code": 200,
    }


@router.delete("/account")
def delete_account(current_user: CurrentUser, service: AuthServiceDep) -> dict:
    # delete uploaded file if exists (best-effort)
    refer_photo = getattr(current_user, "refer_photo", None)
    if refer_photo:
        file_path = Path("uploads") / str(refer_photo)
        if file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass

    email = service.delete_account(current_user.id)
    return {
        "success": True,
        "message": "Account deleted successfully",
        "data": {"email": email},
        "code": 200,
    }
