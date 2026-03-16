"""Ports (interfaces) for the Properties domain."""

from __future__ import annotations

from typing import Any, Protocol, Sequence

from app.schemas.property import PropertyCreate, PropertyUpdate


PropertyRecord = Any  # gradually tighten to a domain entity later


class PropertyRepository(Protocol):
    def list(self, *, skip: int, limit: int) -> Sequence[PropertyRecord]:
        raise NotImplementedError

    def get(self, property_id: int) -> PropertyRecord | None:
        raise NotImplementedError

    def create(self, *, payload: PropertyCreate) -> PropertyRecord:
        raise NotImplementedError

    def update(self, property_id: int, *, payload: PropertyUpdate) -> PropertyRecord | None:
        raise NotImplementedError

    def delete(self, property_id: int) -> bool:
        raise NotImplementedError
