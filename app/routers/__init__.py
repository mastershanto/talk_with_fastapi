"""
Routers package — collect all APIRouter instances.

Import routers from here in main.py:
    from app.routers import users, properties, auth
"""
from app.routers import users, properties, auth

__all__ = ["users", "properties", "auth"]
