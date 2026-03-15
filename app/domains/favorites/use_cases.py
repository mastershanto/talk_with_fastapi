"""Use Cases (application services/orchestration) for Favorites."""

from __future__ import annotations

from typing import Sequence

from app.domains.favorites.entities import Favorite
from app.domains.favorites.ports import FavoritesRepository
from app.domains.properties.ports import PropertyRepository, PropertyRecord
from app.exceptions import NotFoundException


class FavoritesUseCases:
    """Application-level orchestration for favorites."""

    def __init__(self, *, favorites: FavoritesRepository, properties: PropertyRepository) -> None:
        self._favorites = favorites
        self._properties = properties

    def favorite_property(self, *, user_id: int, property_id: int) -> Favorite:
        # Rule: property must exist
        prop = self._properties.get(property_id)
        if not prop:
            raise NotFoundException("Property not found")
        # Idempotent add
        return self._favorites.add(user_id=user_id, property_id=property_id)

    def unfavorite_property(self, *, user_id: int, property_id: int) -> bool:
        # Idempotent remove; do not require property existence.
        return self._favorites.remove(user_id=user_id, property_id=property_id)

    def list_favorites(
        self,
        *,
        user_id: int,
        skip: int,
        limit: int,
    ) -> Sequence[tuple[PropertyRecord, Favorite]]:
        return self._favorites.list_with_properties(user_id=user_id, skip=skip, limit=limit)
