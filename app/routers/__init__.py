"""
Routers package — collect all APIRouter instances.

Import routers from here in main.py:
    from app.routers import users, properties, auth, favorites
"""
from app.routers import users, properties, auth, favorites

__all__ = ["users", "properties", "auth", "favorites"]

