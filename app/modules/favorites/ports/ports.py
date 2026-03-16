"""Ports (interfaces) for the Favorites domain.

Use-cases depend only on these interfaces.
"""

from __future__ import annotations

from typing import Any, Protocol, Sequence

from app.modules.favorites.domain.entities import Favorite


PropertyRecord = Any  # gradually tighten to a domain entity later


class FavoritesRepository(Protocol):
    """Gateway for persisting/querying favorites."""

    def add(self, *, user_id: int, property_id: int) -> Favorite:
        raise NotImplementedError

    def remove(self, *, user_id: int, property_id: int) -> bool:
        """Remove favorite; returns True if something was removed."""
        raise NotImplementedError

    def list_with_properties(
        self,
        *,
        user_id: int,
        skip: int,
        limit: int,
    ) -> Sequence[tuple[PropertyRecord, Favorite]]:
        """Return (property, favorite) pairs for a user."""
        raise NotImplementedError
