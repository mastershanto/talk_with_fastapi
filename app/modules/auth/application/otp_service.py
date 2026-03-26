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

import smtplib
import ssl
import hmac
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BadRequestException, ServiceUnavailableException
from app.persistence.models.otp import EmailOTP


OTP_PURPOSE_REGISTER = "register"
OTP_PURPOSE_FORGOT_PASSWORD = "forgot_password"

OTP_TTL_MINUTES = 10
RESEND_MIN_INTERVAL_SECONDS = 60
MAX_VERIFY_ATTEMPTS = 5


def _utcnow() -> datetime:
    """Return the current UTC time (tz-aware)."""

    return datetime.now(timezone.utc)


def _ensure_utc(dt: datetime) -> datetime:
    """Ensure a datetime is timezone-aware in UTC.

    SQLite may return naive datetimes even if SQLAlchemy is configured with timezone=True.
    """

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


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

    If SMTP is enabled, send via SMTP.
    Otherwise, in DEBUG mode only, print the OTP for local development.
    """
    if not settings.SMTP_ENABLED:
        # Dev-only convenience: never log OTPs in production.
        if settings.DEBUG:
            print(f"[OTP:{purpose}] {email} -> {otp}")
        return

    if not settings.SMTP_HOST:
        raise ServiceUnavailableException("SMTP is enabled but SMTP_HOST is not set")

    from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USERNAME
    if not from_email:
        raise ServiceUnavailableException("SMTP_FROM_EMAIL (or SMTP_USERNAME) must be set")

    if bool(settings.SMTP_USERNAME) ^ bool(settings.SMTP_PASSWORD):
        raise ServiceUnavailableException("SMTP_USERNAME and SMTP_PASSWORD must be set together")

    subject = "Your OTP code"
    body = (
        "Your one-time code is: "
        f"{otp}\n\n"
        f"Purpose: {purpose}\n"
        f"Expires in: {OTP_TTL_MINUTES} minutes\n"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = email
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        if settings.SMTP_USE_SSL:
            with smtplib.SMTP_SSL(
                host=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                timeout=settings.SMTP_TIMEOUT_SECONDS,
                context=context,
            ) as smtp:
                if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                    smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                smtp.send_message(msg)
            return

        with smtplib.SMTP(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            timeout=settings.SMTP_TIMEOUT_SECONDS,
        ) as smtp:
            smtp.ehlo()
            if settings.SMTP_USE_TLS:
                smtp.starttls(context=context)
                smtp.ehlo()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
    except Exception as exc:
        raise ServiceUnavailableException("Failed to send OTP") from exc


def issue_otp(db: Session, *, email: str, purpose: str) -> str:
    """Issue (and send) an OTP for the given email + purpose. Returns the OTP code."""
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
    return otp


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
    expires_at = _ensure_utc(record.expires_at)

    if expires_at <= now:
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
