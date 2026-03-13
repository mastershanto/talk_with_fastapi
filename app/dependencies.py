"""
FastAPI dependency injection functions.

Import the type aliases for concise route signatures:

    from app.dependencies import DBSession, Pagination

    @router.get("/")
    def list_items(db: DBSession, pagination: Pagination): ...
"""
from typing import Annotated, Generator

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal


# ── Database session ──────────────────────────────────────────────────────────

def get_db() -> Generator[Session, None, None]:
    """
    Yield a SQLAlchemy `Session`, ensuring it is always closed after the
    request — even if the handler raises an exception.

    Typical usage (prefer the alias):
        db: DBSession = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotated alias — use `DBSession` as the type hint in route parameters.
DBSession = Annotated[Session, Depends(get_db)]


# ── Pagination ────────────────────────────────────────────────────────────────

class PaginationParams:
    """
    Reusable pagination query-parameter bundle.

    Injects `skip` and `limit` from the query string with sensible defaults
    and server-enforced maximums defined in Settings.
    """

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(
            settings.DEFAULT_PAGE_SIZE,
            ge=1,
            le=settings.MAX_PAGE_SIZE,
            description="Maximum number of records to return",
        ),
    ) -> None:
        self.skip = skip
        self.limit = limit


# Annotated alias — use `Pagination` as the type hint in route parameters.
Pagination = Annotated[PaginationParams, Depends(PaginationParams)]
