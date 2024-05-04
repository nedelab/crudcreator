

from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from typing import Optional
from pydantic import BaseModel
from .CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ..Fields import Fields
from ..FieldOfCRUDableEntityType import FieldOfCRUDableEntityType

class InterfaceDescriptor(BaseModel):
   
    name: str
    can_indicate_read_distinct: bool
    fields: list[FieldOfCRUDableEntityType]


    def build(self) -> CRUDableEntityTypeInterface:
        return CRUDableEntityTypeInterface(
                name=self.name,
                can_indicate_read_distinct=self.can_indicate_read_distinct,
                fields=Fields.build(self.fields)
            )