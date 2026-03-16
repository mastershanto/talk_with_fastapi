"""FastAPI application factory implementation.

This module contains the concrete implementation of the application wiring logic.
Keeping it separate from `app.main` ensures the entrypoint stays minimal and avoids
accidental side effects when importing `app.main` in other contexts (e.g., tooling
or tests that only need configuration values).

Component structure:
- database.py: DatabaseInitializer
- lifespan.py: LifespanManager
- registrars.py: RouterRegistrar, AdminRegistrar, HealthRegistrar
- factory.py: FastAPIApplicationFactory (this file)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.exceptions import register_exception_handlers
from app.core.telemetry import init_telemetry
from app.zmain.database import DatabaseInitializer
from app.zmain.lifespan import LifespanManager
from app.zmain.registrars import RouterRegistrar, AdminRegistrar, HealthRegistrar




class FastAPIApplicationFactory:
    """Encapsulates FastAPI application construction and wiring."""

    def __init__(self) -> None:
        self.settings = settings
        self.db_initializer = DatabaseInitializer(SessionLocal)
        self.lifespan_manager = LifespanManager(self.db_initializer)
        self.router_registrar = RouterRegistrar()
        self.admin_registrar = AdminRegistrar()
        self.health_registrar = HealthRegistrar()

    def create_app(self) -> FastAPI:
        """Construct and configure the FastAPI application."""

        application = FastAPI(
            title=self.settings.APP_NAME,
            description=self.settings.APP_DESCRIPTION,
            version=self.settings.APP_VERSION,
            docs_url="/docs",
            redoc_url="/redoc",
            lifespan=self.lifespan_manager.lifespan,
        )

        # Initialize structured logging and optional OpenTelemetry tracing.
        init_telemetry(application)

        # ── CORS ──────────────────────────────────────────────────────────────────
        application.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # ── Custom exception handlers ──────────────────────────────────────────────
        register_exception_handlers(application)

        # ── Application wiring ───────────────────────────────────────────────────
        self.router_registrar.register(application)
        self.admin_registrar.register(application)
        self.health_registrar.register(application)

        return application


def create_app() -> FastAPI:
    """Factory helper used by tests and uvicorn entrypoints."""

    return FastAPIApplicationFactory().create_app()


# ── Module-level app instance (used by uvicorn) ────────────────────────────────

app: FastAPI = create_app()
