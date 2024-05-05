
from .AbstractProxyParams import AbstractProxyParams
from .ProxyIndex import proxy_index
from .AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ..AbstractDescriptor import AbstractDescriptor
from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from typing import Optional, Type

class ProxyDescriptor(AbstractDescriptor[AbstractCRUDableEntityTypeProxy, AbstractProxyParams]):
   
    base: Optional[AbstractCRUDableEntityType] = None
    """
    The module for which this descriptor will be the proxy.
    """

    addons: dict[str, Type[AbstractCRUDableEntityTypeProxy]]

    def get_index(self) -> dict[str, AbstractCRUDableEntityTypeProxy]:
        return proxy_index
    
    def build(self) -> AbstractCRUDableEntityTypeProxy:
        """
        Builds the proxy associated with the descriptor.
        """
        return self.get_class().build(
            proxy_params=self.get_params(),
            base=self.base
        )