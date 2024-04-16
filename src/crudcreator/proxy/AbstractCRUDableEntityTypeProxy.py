from typing import Any
from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ..interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from .AbstractProxyParams import AbstractProxyParams
from ..schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from ..transaction.AbstractTransaction import AbstractTransaction

class AbstractCRUDableEntityTypeProxy(AbstractCRUDableEntityType):
    """
    Transforms a CRUDable entity type.
    This class must be inherited.
    """

    base: AbstractCRUDableEntityType
    """
    The type of entity to which the proxy plugs in and modifies behavior.
    """

    params: AbstractProxyParams
    """
    Parameters for customizing a proxy.
    It's up to the AbstractProxyParams implementations to build as they should.
    """

    @classmethod
    def build(
        cls,
        proxy_params: AbstractProxyParams,
        base: AbstractCRUDableEntityType
    ) -> "AbstractCRUDableEntityTypeProxy":
        """
        Method to call to instantiate a Proxy.

        :param proxy_params:
            See above.

        :param base:
            See above.
        """
        return cls(
            interface=cls._get_updated_interface(
                base.interface.model_copy(), 
                params=proxy_params
            ),
            base=base,
            params=proxy_params
        )
    
    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: AbstractProxyParams) -> CRUDableEntityTypeInterface:
        """
        ATTENTION : base_interface est supposé être une deep copy de l'interface de la base
        Most often, modifying the CRUD behavior of an entity type involves
        a transformation of its interface (the way the user will see it).
        For example, modifying the way an entity is read will often mean that the user will not read the same thing,
        or that the data read will not have the same format.
        All AbstractCRUDableEntityTypeProxy subclasses will therefore also have to transform
        the interface of the entity type you wish to transform.

        WARNING: base_interface is assumed to be a deep copy of the base interface.
        """
        return base_interface
    
    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Overload if you want to change the read behavior.
        """
        return await self.base.read(params)
    
    async def create(self, params: CreateParams):
        """
        Overload if you want to change the create behavior.
        """
        return await self.base.create(params)
    
    async def delete(self, params: DeleteParams):
        """
        Overload if you want to change the delete behavior.
        """
        return await self.base.delete(params)
    
    async def update(self, params: UpdateParams):
        """
        Overload if you want to change the update behavior.
        """
        return await self.base.update(params)
    