"""
Routers package — collect all APIRouter instances.

Import routers from here in main.py:
    from app.routers import users, items
"""
from app.routers import users, items

__all__ = ["users", "items"]
