from app.repositories.base import CRUDBase
from app.persistence.models.property import Property
from app.modules.properties.schemas.property import PropertyCreate, PropertyUpdate


class CRUDProperty(CRUDBase[Property, PropertyCreate, PropertyUpdate]):
    """
    CRUD operations for properties.
    """
    pass


property_crud = CRUDProperty(Property)
