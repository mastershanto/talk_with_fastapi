"""FastAPI lifespan context manager."""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.core.config import settings
from app.zmain.database import DatabaseInitializer


logger = logging.getLogger(__name__)


class LifespanManager:
    """Provides the FastAPI lifespan handler."""

    def __init__(self, db_initializer: DatabaseInitializer) -> None:
        self._db_initializer = db_initializer

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
        logger.info("Starting %s v%s ...", settings.APP_NAME, settings.APP_VERSION)

        if settings.DB_AUTO_CREATE_TABLES:
            self._db_initializer.create_tables()
        else:
            logger.info("DB auto-create disabled. Run Alembic migrations to manage schema.")

        # self._db_initializer.seed_sample_data()  # Disabled for production readiness
        yield
        logger.info("Shutdown complete.")
