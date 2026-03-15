"""Properties application service (use-cases)."""

from __future__ import annotations

from app.domains.properties.ports import PropertyRepository, PropertyRecord
from app.domains.users.ports import UserRepository
from app.schemas.property import PropertyCreate, PropertyUpdate


class PropertyService:
    def __init__(self, properties: PropertyRepository, users: UserRepository) -> None:
        self._properties = properties
        self._users = users

    def list_properties(self, *, skip: int, limit: int) -> list[PropertyRecord]:
        return list(self._properties.list(skip=skip, limit=limit))

    def get_property(self, property_id: int) -> PropertyRecord | None:
        return self._properties.get(property_id)

    def create_property(self, payload: PropertyCreate) -> PropertyRecord | None:
        owner = self._users.get(payload.owner_id)
        if not owner:
            return None
        return self._properties.create(payload=payload)

    def update_property(self, property_id: int, payload: PropertyUpdate) -> PropertyRecord | None:
        return self._properties.update(property_id, payload=payload)

    def delete_property(self, property_id: int) -> bool:
        return self._properties.delete(property_id)
