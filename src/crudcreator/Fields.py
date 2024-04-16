
from pydantic import BaseModel

class Fields(BaseModel):
    """
    An instance of this class represents the fields of an entity.
    """

    list_field: list["FieldOfCRUDableEntityType"]
    """
    The list of fields.
    """

    index_field_by_name: dict[str, "FieldOfCRUDableEntityType"]
    """
    A name -> field index built by the "build" classmethod.
    """
    
    @classmethod
    def build(cls, list_field: list["FieldOfCRUDableEntityType"]):
        """
        Use this method to build an instance of Fields.

        :param list_field:
            The list of fields.
        """
        return cls(
            list_field=list_field,
            index_field_by_name={
                field.name:field
                for field in list_field
            }
        )
    
from .Link import Link
from .interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from .AbstractCRUDableEntityType import AbstractCRUDableEntityType
from .FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
Fields.model_rebuild()