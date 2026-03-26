"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.modules.auth.api.router`.
"""

from app.modules.auth.api.router import router

__all__ = ["router"]
