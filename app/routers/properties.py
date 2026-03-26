"""Compatibility shim.

The project is moving to a feature-first modular monolith. The real router now
lives at `app.modules.properties.api.router`.
"""

from app.modules.properties.api.router import router

<<<<<<< HEAD
from app.repositories.property import property_crud
from app.repositories.user import user_crud  # Import correctly from app.repositories.user
from app.dependencies import DBSession, Pagination
from app.exceptions import NotFoundException
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from app.response_formatter import success_response, list_response

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get(
    "/",
    summary="List all properties",
)
def list_properties(db: DBSession, pagination: Pagination) -> dict:
    """Return a paginated list of properties."""
    properties = property_crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)
    property_list = [PropertyResponse.model_validate(p) for p in properties]
    return list_response(property_list, message="Properties fetched successfully", code=200)


@router.get(
    "/{property_id}",
    summary="Get a property",
)
def get_property(property_id: int, db: DBSession) -> dict:
    """Return a single property by ID, or 404."""
    prop = property_crud.get(db, property_id)
    if not prop:
        raise NotFoundException(f"Property {property_id} not found.")
    property_data = PropertyResponse.model_validate(prop)
    return success_response(property_data, message="Property fetched successfully", code=200)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a property",
)
def create_property(payload: PropertyCreate, db: DBSession) -> dict:
    """Create a new property listing."""
    # Ensure owner exists
    owner = user_crud.get(db, payload.owner_id)
    if not owner:
        raise NotFoundException(f"Owner (User {payload.owner_id}) not found.")
        
    prop = property_crud.create(db, obj_in=payload)
    property_data = PropertyResponse.model_validate(prop)
    return success_response(property_data, message="Property created successfully", code=201)


@router.put(
    "/{property_id}",
    summary="Update a property",
)
def update_property(property_id: int, payload: PropertyUpdate, db: DBSession) -> dict:
    """Update a property."""
    db_prop = property_crud.get(db, property_id)
    if not db_prop:
        raise NotFoundException(f"Property {property_id} not found.")
    
    updated_prop = property_crud.update(db, db_obj=db_prop, obj_in=payload)
    property_data = PropertyResponse.model_validate(updated_prop)
    return success_response(property_data, message="Property updated successfully", code=200)


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a property",
)
def delete_property(property_id: int, db: DBSession) -> dict:
    """Hard delete a property."""
    db_prop = property_crud.get(db, property_id)
    if not db_prop:
        raise NotFoundException(f"Property {property_id} not found.")
    property_crud.remove(db, record_id=property_id)
    return success_response(data={"id": property_id}, message="Property deleted successfully", code=200)
=======
__all__ = ["router"]
>>>>>>> 7199041aea298502b86585a00da5e2a710d75cd3
