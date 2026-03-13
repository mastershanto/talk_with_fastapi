"""
Property endpoints.

Routes
------
GET    /api/v1/properties            list_properties    — paginated list
GET    /api/v1/properties/{id}       get_property       — single property
POST   /api/v1/properties            create_property    — create property
PUT    /api/v1/properties/{id}       update_property    — partial update
DELETE /api/v1/properties/{id}       delete_property    — hard delete
"""
from fastapi import APIRouter, status

from app.repositories.property import property_crud
from app.repositories.user import user_crud  # Import correctly from app.repositories.user
from app.dependencies import DBSession, Pagination
from app.exceptions import NotFoundException
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get(
    "/",
    response_model=list[PropertyResponse],
    summary="List all properties",
)
def list_properties(db: DBSession, pagination: Pagination) -> list[PropertyResponse]:
    """Return a paginated list of properties."""
    properties = property_crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)
    return [PropertyResponse.model_validate(p) for p in properties]


@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
    summary="Get a property",
)
def get_property(property_id: int, db: DBSession) -> PropertyResponse:
    """Return a single property by ID, or 404."""
    prop = property_crud.get(db, property_id)
    if not prop:
        raise NotFoundException(f"Property {property_id} not found.")
    return PropertyResponse.model_validate(prop)


@router.post(
    "/",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a property",
)
def create_property(payload: PropertyCreate, db: DBSession) -> PropertyResponse:
    """Create a new property listing."""
    # Ensure owner exists
    owner = user_crud.get(db, payload.owner_id)
    if not owner:
        raise NotFoundException(f"Owner (User {payload.owner_id}) not found.")
        
    prop = property_crud.create(db, obj_in=payload)
    return PropertyResponse.model_validate(prop)


@router.put(
    "/{property_id}",
    response_model=PropertyResponse,
    summary="Update a property",
)
def update_property(property_id: int, payload: PropertyUpdate, db: DBSession) -> PropertyResponse:
    """Update a property."""
    db_prop = property_crud.get(db, property_id)
    if not db_prop:
        raise NotFoundException(f"Property {property_id} not found.")
    
    updated_prop = property_crud.update(db, db_obj=db_prop, obj_in=payload)
    return PropertyResponse.model_validate(updated_prop)


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a property",
)
def delete_property(property_id: int, db: DBSession) -> None:
    """Hard delete a property."""
    db_prop = property_crud.get(db, property_id)
    if not db_prop:
        raise NotFoundException(f"Property {property_id} not found.")
    property_crud.remove(db, record_id=property_id)
