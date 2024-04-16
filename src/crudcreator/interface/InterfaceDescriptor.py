

from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from typing import Optional
from pydantic import BaseModel
from .CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ..Fields import Fields
from ..FieldOfCRUDableEntityType import FieldOfCRUDableEntityType

class InterfaceDescriptor(BaseModel):
   
    name: str
    fields: list[FieldOfCRUDableEntityType]


    def build(self) -> CRUDableEntityTypeInterface:
        return CRUDableEntityTypeInterface(
                name=self.name,
                fields=Fields.build(self.fields)
            )