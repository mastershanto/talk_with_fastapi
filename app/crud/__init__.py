"""
CRUD package — exposes domain CRUD singletons.

Usage:
    from app.crud import user_crud, property_crud
"""
from app.crud.user import user_crud
from app.crud.property import property_crud

__all__ = ["user_crud", "property_crud"]
