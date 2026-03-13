"""
Routers package — collect all APIRouter instances.

Import routers from here in main.py:
    from app.routers import users, properties
"""
from app.routers import users, properties

__all__ = ["users", "properties"]
