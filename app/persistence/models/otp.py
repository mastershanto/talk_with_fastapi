"""Email OTP model.

Stores one-time passcodes for email verification and password reset flows.
Codes are stored as a hash (never plaintext) and are single-use.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class EmailOTP(TimestampMixin, Base):
    """One-time passcode bound to an email + purpose."""

    __tablename__ = "email_otps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    purpose: Mapped[str] = mapped_column(String(50), index=True, nullable=False)

    code_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    verify_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def is_consumed(self) -> bool:
        return self.consumed_at is not None
