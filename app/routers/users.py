"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.modules.users.api.router`.
"""

from app.modules.users.api.router import router

__all__ = ["router"]
