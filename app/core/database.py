"""
Database engine, session factory, and declarative base.

Public surface:
    engine       — SQLAlchemy Engine (table creation / Alembic migrations)
    SessionLocal — sessionmaker factory (injected via app.dependencies.get_db)
    Base         — DeclarativeBase for all ORM models

Do NOT import `get_db` from here — use `app.dependencies` instead.
"""
import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool

from app.config import settings

logger = logging.getLogger(__name__)


# ── Engine factory ────────────────────────────────────────────────────────────

def _build_engine() -> Engine:
    """Build and return a SQLAlchemy engine from the current Settings."""
    url = settings.DATABASE_URL

    if url.startswith("sqlite"):
        # SQLite: NullPool + allow multi-thread access (needed for tests)
        logger.debug("Engine: SQLite (NullPool)")
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=NullPool,
            echo=settings.DB_ECHO,
        )

    # PostgreSQL (or any other server-side DB)
    logger.debug("Engine: PostgreSQL (pool_size=%d)", settings.DB_POOL_SIZE)
    return create_engine(
        url,
        connect_args={
            "connect_timeout": 10,
            "options": "-c statement_timeout=30000",
        },
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=settings.DB_POOL_PRE_PING,
        echo=settings.DB_ECHO,
    )


engine = _build_engine()


# ── Session factory ───────────────────────────────────────────────────────────

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # avoids implicit lazy-loads after commit
)


# ── Declarative base ──────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    """Project-wide declarative base — every ORM model must inherit from this."""

    pass


# ── Legacy helper (kept for backward-compat; prefer app.dependencies.get_db) ──

def get_db():  # pragma: no cover
    """Yield a DB session. Prefer injecting DBSession from app.dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
