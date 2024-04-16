from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from .CRUDableEntityBuilder import CRUDableEntityBuilder
from typing import Any
from pydantic import BaseModel
from ..source.AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ..proxy.AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy

class EntityDescriptor(BaseModel):#TODO : changer de nom ?
    path: str
    """
    The path of the json file from which to build the entity.
    """

    export: bool
    """
    Should the built entity be returned by the build function?
    """

class SetBuilder():
    """
    Allows multiple entity types to be constructed.
    Useful when entities refer to each other.
    """

    async def build(
        self, 
        list_entity_descriptor: list[EntityDescriptor], 
        subs_index: dict[str, Any], 
        addon_source: dict[str, AbstractCRUDableEntityTypeSource], 
        addon_proxy: dict[str, AbstractCRUDableEntityTypeProxy]
    ) -> list[AbstractCRUDableEntityType]:
        """
        Builds multiple entity types from a list of .json files.
        Stores in an index references as it encounters them, which it merges with subs_index.

        :param list_entity_descriptor:
            The list of json files.

        :param subs_index:
            An index that indicates the corresponding Python object for variables in descriptors.

        :param addon_source:
            An index of the library user's custom source modules.

        :param addon_proxy:
            An index of the library user's custom proxy modules.
        """
        list_crud = []
        ref = {}
        for entity_descriptor in list_entity_descriptor:
            builder = CRUDableEntityBuilder(None)
            builder_ref = await builder.from_file(
                entity_descriptor.path,
                {
                    **ref,
                    **subs_index
                },
                addon_source,
                addon_proxy
            )
            ref = {**ref, **builder_ref}
            if entity_descriptor.export:
                list_crud.append(builder.get_built_entity())
        return list_crud