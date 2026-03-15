from __future__ import annotations

import pytest

from app.config import Settings


def test_settings_rejects_unsafe_production_defaults() -> None:
    with pytest.raises(ValueError):
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="short",
            ALLOWED_ORIGINS=["*"],
            DB_AUTO_CREATE_TABLES=True,
        )


def test_settings_accepts_safe_production_config() -> None:
    s = Settings(
        ENVIRONMENT="production",
        SECRET_KEY="x" * 40,
        ALLOWED_ORIGINS=["https://example.com"],
        DB_AUTO_CREATE_TABLES=False,
        OTEL_SAMPLE_RATE=0.5,
    )
    assert s.ENVIRONMENT == "production"
