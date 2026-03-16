from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.modules.auth.infrastructure.sqlalchemy.auth import SqlAlchemyAuthRepository
from app.persistence.models.user import User


def _build_sessionmaker() -> tuple[sessionmaker, Engine]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    User.metadata.create_all(bind=engine)
    return (
        sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False),
        engine,
    )


def test_auth_adapter_create_and_verify_credentials() -> None:
    SessionLocal, engine = _build_sessionmaker()
    db = SessionLocal()
    repo = SqlAlchemyAuthRepository(db)

    user = repo.create_user(
        email="  Test@Example.com ",
        password="Secret123",
        name="Test",
        role="user",
        agree_to_terms=True,
        is_premium=False,
    )

    assert user.email == "test@example.com"
    assert repo.verify_user_credentials("test@example.com", "Secret123") is not None
    assert repo.verify_user_credentials("test@example.com", "WrongSecret") is None

    db.close()
    engine.dispose()


def test_auth_adapter_mark_verified_and_tokens() -> None:
    SessionLocal, engine = _build_sessionmaker()
    db = SessionLocal()
    repo = SqlAlchemyAuthRepository(db)

    user = repo.create_user(
        email="v@example.com",
        password="Secret123",
        name="Verifier",
        role="user",
        agree_to_terms=True,
        is_premium=False,
    )

    assert user.email_verified_at is None
    user = repo.mark_email_verified(user)
    assert user.email_verified_at is not None

    login_token = repo.generate_login_token(user)
    reset_token = repo.generate_password_reset_token(user)

    assert isinstance(login_token, str) and len(login_token) > 10
    assert isinstance(reset_token, str) and len(reset_token) > 10

    db.close()
    engine.dispose()
