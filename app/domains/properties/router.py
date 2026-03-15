"""Properties HTTP adapter (FastAPI router)."""

from fastapi import APIRouter, status

from app.dependencies import Pagination, PropertyServiceDep
from app.exceptions import NotFoundException
from app.response_formatter import list_response, success_response
from app.schemas.property import PropertyCreate, PropertyResponse, PropertyUpdate

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get(
    "/",
    summary="List all properties",
)
def list_properties(service: PropertyServiceDep, pagination: Pagination) -> dict:
    properties = service.list_properties(skip=pagination.skip, limit=pagination.limit)
    property_list = [PropertyResponse.model_validate(p) for p in properties]
    return list_response(property_list, message="Properties fetched successfully", code=200)


@router.get(
    "/{property_id}",
    summary="Get a property",
)
def get_property(property_id: int, service: PropertyServiceDep) -> dict:
    prop = service.get_property(property_id)
    if not prop:
        raise NotFoundException(f"Property {property_id} not found.")
    property_data = PropertyResponse.model_validate(prop)
    return success_response(property_data, message="Property fetched successfully", code=200)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a property",
)
def create_property(payload: PropertyCreate, service: PropertyServiceDep) -> dict:
    prop = service.create_property(payload)
    if not prop:
        raise NotFoundException(f"Owner (User {payload.owner_id}) not found.")
    property_data = PropertyResponse.model_validate(prop)
    return success_response(property_data, message="Property created successfully", code=201)


@router.put(
    "/{property_id}",
    summary="Update a property",
)
def update_property(property_id: int, payload: PropertyUpdate, service: PropertyServiceDep) -> dict:
    updated_prop = service.update_property(property_id, payload)
    if not updated_prop:
        raise NotFoundException(f"Property {property_id} not found.")
    property_data = PropertyResponse.model_validate(updated_prop)
    return success_response(property_data, message="Property updated successfully", code=200)


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a property",
)
def delete_property(property_id: int, service: PropertyServiceDep) -> dict:
    ok = service.delete_property(property_id)
    if not ok:
        raise NotFoundException(f"Property {property_id} not found.")
    return success_response(data={"id": property_id}, message="Property deleted successfully", code=200)
