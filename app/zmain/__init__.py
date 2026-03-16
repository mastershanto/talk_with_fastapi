"""Reusable factory components (database, lifespan, registrars).

All logic is consolidated in app.main. This module provides backward compatibility
by re-exporting the create_app function.
"""


def create_app():
    """Backward-compatible factory function."""
    from app.main import _Factory
    return _Factory().build()


__all__ = ["create_app"]
