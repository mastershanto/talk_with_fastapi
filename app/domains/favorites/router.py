"""Interface adapters: HTTP controller (FastAPI router) for Favorites."""

from __future__ import annotations

from fastapi import APIRouter

from app.dependencies import FavoritesUseCasesDep, Pagination
from app.response_formatter import success_response
from app.security import CurrentUser
from app.domains.favorites.schemas import FavoritePropertyResponse
from app.schemas.property import PropertyResponse


router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/{property_id}")
def add_favorite(property_id: int, current_user: CurrentUser, use_cases: FavoritesUseCasesDep) -> dict:
    fav = use_cases.favorite_property(user_id=current_user.id, property_id=property_id)
    return success_response(
        data={"property_id": fav.property_id, "favorited_at": fav.favorited_at},
        message="Favorited",
        code=200,
    )


@router.delete("/{property_id}")
def remove_favorite(property_id: int, current_user: CurrentUser, use_cases: FavoritesUseCasesDep) -> dict:
    use_cases.unfavorite_property(user_id=current_user.id, property_id=property_id)
    return success_response(
        data={"property_id": property_id},
        message="Unfavorited",
        code=200,
    )


@router.get("/")
def list_favorites(
    current_user: CurrentUser,
    pagination: Pagination,
    use_cases: FavoritesUseCasesDep,
) -> dict:
    rows = use_cases.list_favorites(user_id=current_user.id, skip=pagination.skip, limit=pagination.limit)

    items = [
        FavoritePropertyResponse(
            property=PropertyResponse.model_validate(prop),
            favorited_at=fav.favorited_at,
        ).model_dump()
        for prop, fav in rows
    ]
    return success_response(data=items, message="Favorites retrieved", code=200)

