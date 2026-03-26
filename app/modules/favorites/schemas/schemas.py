"""Interface adapters: DTOs/presenters for Favorites."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.modules.properties.schemas.property import PropertyResponse


class FavoritePropertyResponse(BaseModel):
    property: PropertyResponse
    favorited_at: datetime
