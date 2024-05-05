

from .AdaptatorIndex import adaptator_index
from .AbstractAdaptator import AbstractAdaptator, AbstractAdaptatorParams
from ..AbstractDescriptor import AbstractDescriptor
from ..interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ..interface.InterfaceDescriptor import InterfaceDescriptor
from typing import Type

class AdaptatorDescriptor(AbstractDescriptor[AbstractAdaptator, AbstractAdaptatorParams]):
    
    interface: dict
    addons: dict[str, Type[AbstractAdaptator]]

    def get_index(self) -> dict[str, AbstractAdaptator]:
        return adaptator_index
    
    def build(self) -> AbstractAdaptator:
        """
        Builds the adaptator associated with the descriptor.
        """
        return self.get_class().build(
            source_params=self.get_params(),
            interface=InterfaceDescriptor(**self._get_params_dict_subst(self.interface)).build()
        )