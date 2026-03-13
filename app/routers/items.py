"""
Item endpoints.

Routes
------
GET    /api/v1/items            list_items    — paginated list
GET    /api/v1/items/{id}       get_item      — single item
POST   /api/v1/items            create_item   — create (owner must exist)
PUT    /api/v1/items/{id}       update_item   — partial update (no owner change)
DELETE /api/v1/items/{id}       delete_item   — hard delete
"""
from fastapi import APIRouter, status

from app.crud import item_crud, user_crud
from app.dependencies import DBSession, Pagination
from app.exceptions import BadRequestException, NotFoundException
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.get(
    "/",
    response_model=list[ItemResponse],
    summary="List all items",
)
def list_items(db: DBSession, pagination: Pagination) -> list[ItemResponse]:
    """Return a paginated list of items."""
    return item_crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get an item",
)
def get_item(item_id: int, db: DBSession) -> ItemResponse:
    """Return a single item by ID, or 404 if not found."""
    item = item_crud.get(db, item_id)
    if not item:
        raise NotFoundException(f"Item {item_id} not found.")
    return item


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
)
def create_item(payload: ItemCreate, db: DBSession) -> ItemResponse:
    """
    Create a new item.

    The owner specified by `owner_id` must already exist — a 400 is returned
    otherwise.
    """
    if not user_crud.get(db, payload.owner_id):
        raise BadRequestException(f"Owner with id {payload.owner_id} does not exist.")
    return item_crud.create(db, obj_in=payload)


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update an item",
)
def update_item(item_id: int, payload: ItemUpdate, db: DBSession) -> ItemResponse:
    """
    Partially update an item.

    `owner_id` cannot be changed via this endpoint.
    Only explicitly provided fields are updated.
    """
    db_item = item_crud.get(db, item_id)
    if not db_item:
        raise NotFoundException(f"Item {item_id} not found.")
    return item_crud.update(db, db_obj=db_item, obj_in=payload)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
def delete_item(item_id: int, db: DBSession) -> None:
    """Hard-delete an item by ID."""
    db_item = item_crud.get(db, item_id)
    if not db_item:
        raise NotFoundException(f"Item {item_id} not found.")
    item_crud.remove(db, record_id=item_id)
