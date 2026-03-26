"""
ORM models package.

Import all models here so SQLAlchemy's mapper registry can resolve
forward-reference strings (e.g. the "Item" string in User.items) before
any query is executed.

Usage anywhere in the project:
    from app.persistence.models import User, Property
"""
from app.persistence.models.user import User
from app.persistence.models.property import Property
from app.persistence.models.otp import EmailOTP
from app.persistence.models.favorite import PropertyFavorite

__all__ = ["User", "Property", "EmailOTP", "PropertyFavorite"]

