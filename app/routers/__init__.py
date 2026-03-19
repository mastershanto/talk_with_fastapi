"""
Routers package — collect all APIRouter instances.

Import routers from here in main.py:
    from app.routers import users, properties, auth, favorites, iris_talk
"""
from app.routers import users, properties, auth, favorites, iris_talk

__all__ = ["users", "properties", "auth", "favorites", "iris_talk"]

