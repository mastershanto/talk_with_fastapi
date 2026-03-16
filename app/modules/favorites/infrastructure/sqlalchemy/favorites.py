"""Frameworks & Drivers: SQLAlchemy adapter for Favorites."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domains.favorites.entities import Favorite
from app.domains.favorites.ports import FavoritesRepository
from app.models.favorite import PropertyFavorite
from app.models.property import Property


class SqlAlchemyFavoritesRepository(FavoritesRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, *, user_id: int, property_id: int) -> Favorite:
        existing = self._db.scalar(
            select(PropertyFavorite).where(
                PropertyFavorite.user_id == user_id,
                PropertyFavorite.property_id == property_id,
            )
        )
        if existing:
            return Favorite(user_id=user_id, property_id=property_id, favorited_at=existing.created_at)

        row = PropertyFavorite(user_id=user_id, property_id=property_id)
        self._db.add(row)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            # In case of a race, re-read and return idempotently.
            again = self._db.scalar(
                select(PropertyFavorite).where(
                    PropertyFavorite.user_id == user_id,
                    PropertyFavorite.property_id == property_id,
                )
            )
            if again:
                return Favorite(user_id=user_id, property_id=property_id, favorited_at=again.created_at)
            raise

        self._db.refresh(row)
        return Favorite(user_id=user_id, property_id=property_id, favorited_at=row.created_at)

    def remove(self, *, user_id: int, property_id: int) -> bool:
        row = self._db.scalar(
            select(PropertyFavorite).where(
                PropertyFavorite.user_id == user_id,
                PropertyFavorite.property_id == property_id,
            )
        )
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def list_with_properties(
        self,
        *,
        user_id: int,
        skip: int,
        limit: int,
    ) -> Sequence[tuple[Property, Favorite]]:
        stmt = (
            select(Property, PropertyFavorite)
            .join(PropertyFavorite, PropertyFavorite.property_id == Property.id)
            .where(PropertyFavorite.user_id == user_id)
            .order_by(PropertyFavorite.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        rows = self._db.execute(stmt).all()
        return [
            (
                prop,
                Favorite(
                    user_id=user_id,
                    property_id=prop.id,
                    favorited_at=fav.created_at,
                ),
            )
            for prop, fav in rows
        ]

