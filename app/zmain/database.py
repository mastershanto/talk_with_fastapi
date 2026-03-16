"""Database initialization handler."""

import logging
import signal
import threading
import types

from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, engine


logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handles DB schema initialization and (optional) seed data."""

    def __init__(self, session_local: sessionmaker[Session]) -> None:
        self._session_local = session_local

    def create_tables(self) -> None:
        """Create all ORM tables, including a short timeout in the main thread."""
        # Import models so their metadata is registered on Base before create_all
        from app.persistence import models  # noqa: F401

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

    def seed_sample_data(self) -> None:
        """Insert a small set of sample rows if the users table is empty."""
        from app.persistence.models.user import User

        db = self._session_local()
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
