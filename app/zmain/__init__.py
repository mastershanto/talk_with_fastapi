"""Secondary entrypoint package for the FastAPI application.

This package is intended to house the concrete application factory implementation
while keeping `app.main` minimal and stable for deployment, tooling, and tests.

The package is deliberately named `zmain` to remain low-priority in imports and to
prevent clashes with the main `app.main` entrypoint.

Usage:
    from app.zmain import create_app
    app = create_app()
"""

from .factory import create_app

__all__ = ["create_app"]
