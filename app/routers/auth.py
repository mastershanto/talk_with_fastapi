"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.domains.auth.router`.
"""

from app.domains.auth.router import router

__all__ = ["router"]
