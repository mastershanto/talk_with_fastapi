"""SQLAlchemy-backed OTP service adapter."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.auth.ports import OtpService
from app.otp_service import issue_otp, verify_otp


class SqlAlchemyOtpService(OtpService):
    def __init__(self, db: Session) -> None:
        self._db = db

    def issue(self, *, email: str, purpose: str) -> str:
        return issue_otp(self._db, email=email, purpose=purpose)

    def verify(self, *, email: str, purpose: str, otp: str) -> bool:
        return verify_otp(self._db, email=email, purpose=purpose, otp=otp)
