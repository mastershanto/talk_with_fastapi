from app.crud.base import CRUDBase
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate


class CRUDProperty(CRUDBase[Property, PropertyCreate, PropertyUpdate]):
    """
    CRUD operations for properties.
    """
    pass


property_crud = CRUDProperty(Property)
