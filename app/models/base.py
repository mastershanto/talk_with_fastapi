"""
Shared model mixins.

Usage:
    from app.models.base import TimestampMixin

    class MyModel(TimestampMixin, Base):
        ...
"""
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, MappedColumn


class TimestampMixin:
    """
    Adds `created_at` and `updated_at` audit columns to any ORM model.

    Both columns are managed entirely at the database level (server-side
    defaults / on-update triggers via SQLAlchemy), so no application code
    needs to set them explicitly.
    """

    created_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
