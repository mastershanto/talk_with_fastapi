"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.domains.favorites.router`.
"""

from app.domains.favorites.router import router

__all__ = ["router"]
