"""
Repository package — exposes domain repository singletons.

Usage:
    from app.repositories import user_crud, property_crud
"""
from app.repositories.user import user_crud
from app.repositories.property import property_crud

__all__ = ["user_crud", "property_crud"]
