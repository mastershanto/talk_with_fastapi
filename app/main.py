"""
FastAPI application factory.

Entry-point
-----------
Development:
    uvicorn app.main:app --reload

Production:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

The `create_app()` factory is separated from the `app` module-level instance
so the same factory can be called in tests with different settings.
"""
import logging
import signal
import threading
import types
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine, SessionLocal
from app.exceptions import register_exception_handlers
from app.routers import users, properties, auth, favorites
from sqladmin import Admin, ModelView
from app.models.user import User
from app.models.property import Property


# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Startup helpers ───────────────────────────────────────────────────────────

def _create_tables() -> None:
    """
    Create all ORM tables.

    Uses a SIGALRM-based timeout guard only when called from the main thread
    (POSIX only; signal.alarm raises ValueError in non-main threads such as
    those spawned by TestClient).  In non-main-thread contexts the timeout is
    simply omitted — database creation should still succeed or fail fast.
    """
    # Import models so their metadata is registered on Base before create_all
    from app.models import User, Property  # noqa: F401
    in_main_thread = threading.current_thread() is threading.main_thread()

    if in_main_thread:
        def _on_timeout(signum: int, frame: types.FrameType | None) -> None:
            raise TimeoutError("Database init timed out after 15 s")

        signal.signal(signal.SIGALRM, _on_timeout)
        signal.alarm(15)

    try:
        Base.metadata.create_all(bind=engine)
        if in_main_thread:
            signal.alarm(0)
        logger.info("Database tables verified / created.")
    except TimeoutError:
        signal.alarm(0)
        logger.warning("DB init timed out — skipping. Run migrations manually.")
    except Exception as exc:
        if in_main_thread:
            signal.alarm(0)
        logger.warning("DB init error (%s: %s) — continuing.", type(exc).__name__, exc)


def _seed_sample_data() -> None:
    """
    Insert a small set of sample rows if the users table is empty.

    This is a development convenience only — do NOT use in production.
    Gate behind a feature flag (e.g. DEBUG=true) if you need it long-term.
    """
    from app.models import User

    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            sample = [
                User(name="Alice", age=25),
                User(name="Bob", age=30),
                User(name="Charlie", age=35),
            ]
            db.add_all(sample)
            db.commit()
            logger.info("Seeded %d sample users.", len(sample))
    except Exception as exc:
        db.rollback()
        logger.warning("Seeding failed (%s) — skipping.", exc)
    finally:
        db.close()


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Run startup tasks before yielding, then shutdown tasks after."""
    logger.info("Starting %s v%s ...", settings.APP_NAME, settings.APP_VERSION)
    _create_tables()
    # _seed_sample_data()  # Skipped for production readiness
    yield
    logger.info("Shutdown complete.")


# ── Application factory ───────────────────────────────────────────────────────

def create_app() -> FastAPI:
    """
    Construct and configure the FastAPI application.

    Separated as a factory so tests can instantiate the app independently,
    e.g. with a different DATABASE_URL pointing to an in-memory SQLite DB.
    """
    application = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Custom exception handlers ──────────────────────────────────────────────
    register_exception_handlers(application)

    # ── API routers ────────────────────────────────────────────────────────────
    API_PREFIX = "/api/v1"
    application.include_router(auth.router, prefix=API_PREFIX)
    application.include_router(users.router, prefix=API_PREFIX)
    application.include_router(properties.router, prefix=API_PREFIX)
    application.include_router(favorites.router, prefix=API_PREFIX)

    # ── Admin Panel ────────────────────────────────────────────────────────────
    admin = Admin(application, engine)
    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.name, User.age]

    class PropertyAdmin(ModelView, model=Property):
        column_list = [Property.id, Property.title, Property.price, Property.status, Property.owner_id]

    admin.add_view(UserAdmin)
    admin.add_view(PropertyAdmin)

    # ── Health / utility endpoints ─────────────────────────────────────────────

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
        from app.dependencies import get_db

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

    return application


# ── Module-level app instance (used by uvicorn) ────────────────────────────────

app: FastAPI = create_app()
