
from .AbstractSourceParams import AbstractSourceParams
from .SourceIndex import source_index
from .AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ..AbstractDescriptor import AbstractDescriptor
from ..interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ..interface.InterfaceDescriptor import InterfaceDescriptor
from typing import Type

class SourceDescriptor(AbstractDescriptor[AbstractCRUDableEntityTypeSource, AbstractSourceParams]):
    
    interface: dict
    addons: dict[str, Type[AbstractCRUDableEntityTypeSource]]

    def get_index(self) -> AbstractCRUDableEntityTypeSource:
        return source_index
    
    def build(self) -> AbstractCRUDableEntityTypeSource:
        return self.get_class()(
            params=self.get_params(),
            interface=InterfaceDescriptor(**self._get_params_dict_subst(self.interface)).build()
        )