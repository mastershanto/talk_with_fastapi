"""
CRUD package — exposes domain CRUD singletons.

Usage:
    from app.crud import user_crud, item_crud
"""
from app.crud.user import user_crud
from app.crud.item import item_crud

__all__ = ["user_crud", "item_crud"]
