"""
ORM models package.

Import all models here so SQLAlchemy's mapper registry can resolve
forward-reference strings (e.g. the "Item" string in User.items) before
any query is executed.

Usage anywhere in the project:
    from app.models import User, Item
"""
from app.models.user import User
from app.models.item import Item

__all__ = ["User", "Item"]
