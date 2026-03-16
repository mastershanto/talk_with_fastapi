"""Entities (core domain model + rules) for Favorites."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Favorite:
    """Domain entity representing a user's favorite of a property."""

    user_id: int
    property_id: int
    favorited_at: datetime
