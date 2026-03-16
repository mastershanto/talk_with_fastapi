"""Feature registrars for wiring routers, admin, and health endpoints."""

from fastapi import FastAPI
from sqlalchemy import text
import logging

from app.core.config import settings
from app.core.database import engine
from app.routers import users, properties, auth, favorites
from sqladmin import Admin, ModelView
from app.persistence.models.user import User
from app.persistence.models.property import Property
from app.core.dependencies import get_db


logger = logging.getLogger(__name__)


class RouterRegistrar:
    """Registers FastAPI routers for each feature module."""

    def register(self, application: FastAPI) -> None:
        from app.core.version import API_PREFIX

        application.include_router(auth.router, prefix=API_PREFIX)
        application.include_router(users.router, prefix=API_PREFIX)
        application.include_router(properties.router, prefix=API_PREFIX)
        application.include_router(favorites.router, prefix=API_PREFIX)


class AdminRegistrar:
    """Registers SQLAdmin views."""

    def register(self, application: FastAPI) -> None:
        admin = Admin(application, engine)

        class UserAdmin(ModelView, model=User):
            column_list = [User.id, User.name, User.age]

        class PropertyAdmin(ModelView, model=Property):
            column_list = [Property.id, Property.title, Property.price, Property.status, Property.owner_id]

        admin.add_view(UserAdmin)
        admin.add_view(PropertyAdmin)


class HealthRegistrar:
    """Registers lightweight health endpoints."""

    def register(self, application: FastAPI) -> None:
        @application.get("/", tags=["Health"], summary="Root")
        def root() -> dict:
            return {
                "status": "ok",
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "docs": "/docs",
            }

        @application.get("/health", tags=["Health"], summary="Liveness probe")
        def health() -> dict:
            """Kubernetes / load-balancer liveness check."""
            return {"status": "healthy"}

        @application.get("/health/db", tags=["Health"], summary="Database readiness probe")
        def health_db() -> dict:
            """Kubernetes readiness check — verifies the DB connection is alive."""
            db = next(get_db())
            try:
                url = settings.DATABASE_URL
                if url.startswith("sqlite"):
                    version = db.execute(text("SELECT sqlite_version();")).scalar_one_or_none()
                else:
                    version = db.execute(text("SELECT version();")).scalar_one_or_none()
                return {"status": "healthy", "db_version": version}
            finally:
                db.close()
