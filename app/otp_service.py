"""OTP issuance/verification service.

Design goals:
- Store OTP codes hashed (never plaintext)
- Single active OTP per (email, purpose)
- Expiration + single-use
- Simple resend throttling

Email delivery is abstracted behind `send_otp` which currently logs.
Replace with a real provider (SES/SendGrid/etc.) in production.
"""

from __future__ import annotations

import hmac
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.exceptions import BadRequestException
from app.models.otp import EmailOTP


OTP_PURPOSE_REGISTER = "register"
OTP_PURPOSE_FORGOT_PASSWORD = "forgot_password"

OTP_TTL_MINUTES = 10
RESEND_MIN_INTERVAL_SECONDS = 60
MAX_VERIFY_ATTEMPTS = 5


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _hash_otp(*, email: str, purpose: str, otp: str) -> str:
    """Hash OTP using HMAC-SHA256 with SECRET_KEY as key."""
    msg = f"{_normalize_email(email)}|{purpose}|{otp}".encode("utf-8")
    key = settings.SECRET_KEY.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def _generate_otp() -> str:
    """Generate a 6-digit numeric OTP."""
    return f"{secrets.randbelow(1_000_000):06d}"


def send_otp(email: str, purpose: str, otp: str) -> None:
    """Deliver OTP to the user.

    Current implementation logs the OTP for local development.
    Replace with a real email provider in production.
    """
    # Intentionally prints minimal context. In production, do NOT log OTPs.
    print(f"[OTP:{purpose}] {email} -> {otp}")


def issue_otp(db: Session, *, email: str, purpose: str) -> None:
    """Issue (and send) an OTP for the given email + purpose."""
    normalized_email = _normalize_email(email)

    # Throttle resends: check the most recent OTP.
    latest_stmt = (
        select(EmailOTP)
        .where(EmailOTP.email == normalized_email, EmailOTP.purpose == purpose)
        .order_by(EmailOTP.created_at.desc())
        .limit(1)
    )
    latest = db.scalar(latest_stmt)
    if latest and (latest.created_at is not None):
        delta = _utcnow() - latest.created_at
        if delta.total_seconds() < RESEND_MIN_INTERVAL_SECONDS:
            raise BadRequestException("Please wait before requesting another OTP.")

    # Invalidate any previously active OTP.
    active_stmt = (
        select(EmailOTP)
        .where(
            EmailOTP.email == normalized_email,
            EmailOTP.purpose == purpose,
            EmailOTP.consumed_at.is_(None),
            EmailOTP.expires_at > _utcnow(),
        )
        .order_by(EmailOTP.created_at.desc())
    )
    for old in db.scalars(active_stmt).all():
        old.consumed_at = _utcnow()

    otp = _generate_otp()
    code_hash = _hash_otp(email=normalized_email, purpose=purpose, otp=otp)
    expires_at = _utcnow() + timedelta(minutes=OTP_TTL_MINUTES)

    db.add(
        EmailOTP(
            email=normalized_email,
            purpose=purpose,
            code_hash=code_hash,
            expires_at=expires_at,
            consumed_at=None,
            verify_attempts=0,
        )
    )
    db.commit()

    send_otp(normalized_email, purpose, otp)


def verify_otp(db: Session, *, email: str, purpose: str, otp: str) -> bool:
    """Verify and consume an OTP.

    Returns True on success, False on invalid/expired OTP.
    """
    normalized_email = _normalize_email(email)

    stmt = (
        select(EmailOTP)
        .where(
            EmailOTP.email == normalized_email,
            EmailOTP.purpose == purpose,
            EmailOTP.consumed_at.is_(None),
        )
        .order_by(EmailOTP.created_at.desc())
        .limit(1)
    )
    record = db.scalar(stmt)
    if not record:
        return False

    now = _utcnow()
    if record.expires_at <= now:
        record.consumed_at = now
        db.commit()
        return False

    if record.verify_attempts >= MAX_VERIFY_ATTEMPTS:
        record.consumed_at = now
        db.commit()
        return False

    expected = record.code_hash
    actual = _hash_otp(email=normalized_email, purpose=purpose, otp=otp)

    record.verify_attempts += 1

    if not hmac.compare_digest(expected, actual):
        db.commit()
        return False

    record.consumed_at = now
    db.commit()
    return True
