"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.domains.properties.router`.
"""

from app.domains.properties.router import router

__all__ = ["router"]
