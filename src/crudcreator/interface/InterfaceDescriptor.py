

from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from typing import Optional
from pydantic import BaseModel
from .CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ..Fields import Fields
from ..FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ..Sentinel import Sentinel

class InterfaceDescriptor(BaseModel):
   
    name: str
    can_indicate_read_distinct: bool
    fields: Optional[list[FieldOfCRUDableEntityType]] = Sentinel.unknown


    def build(self) -> CRUDableEntityTypeInterface:
        return CRUDableEntityTypeInterface(
                name=self.name,
                can_indicate_read_distinct=self.can_indicate_read_distinct,
                fields=Fields.build(self.fields) if self.fields != Sentinel.unknown else Sentinel.unknown
            )