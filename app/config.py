"""
Application configuration via pydantic-settings.

All settings are readable from environment variables or a `.env` file.
Use `from app.config import settings` anywhere in the project.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration object for the entire application.

    Override any value by setting the corresponding env-var, e.g.:
        DATABASE_URL=postgresql://... DEBUG=true uvicorn app.main:app
    """

    # ── Application ───────────────────────────────────────────────────────────
    APP_NAME: str = "Real Estate Enterprise API"
    APP_DESCRIPTION: str = "Enterprise-grade Property Management System"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/real_estate_db"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_PRE_PING: bool = True
    DB_ECHO: bool = False  # Set True to log every SQL statement

    # Safety switch: in production, prefer running `alembic upgrade head`.
    # Tests/dev can set DB_AUTO_CREATE_TABLES=true.
    DB_AUTO_CREATE_TABLES: bool = False

    # ── CORS ──────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = ["*"]

    # ── Pagination ────────────────────────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # ── Authentication ────────────────────────────────────────────────────────
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ── Observability / Tracing ──────────────────────────────────────────────
    OTEL_ENABLED: bool = False
    OTEL_SERVICE_NAME: str = "talk-with-fastapi"
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = None
    OTEL_SAMPLE_RATE: float = 0.1

    # ── Environment
    ENVIRONMENT: str = "development"

    # ── Secret store (Vault/KV etc.)
    VAULT_URL: str | None = None
    VAULT_TOKEN: str | None = None

    # ── pydantic-settings meta ─────────────────────────────────────────────────
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton Settings instance (cached after first call)."""
    # Load optional secrets from external vault before instantiating settings.
    try:
        from app.secrets import load_vault_secrets

        load_vault_secrets()
    except Exception:
        # Keep it silent — failure to reach Vault should not block startup.
        pass

    return Settings()


# Module-level singleton — import this everywhere.
settings: Settings = get_settings()
