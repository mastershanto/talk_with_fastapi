"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.modules.properties.api.router`.
"""

from app.modules.properties.api.router import router

__all__ = ["router"]
