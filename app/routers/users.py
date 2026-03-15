"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.domains.users.router`.
"""

from app.domains.users.router import router

__all__ = ["router"]
