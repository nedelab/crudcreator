

from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ..proxy.AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ..proxy.AbstractProxyParams import AbstractProxyParams
from ..proxy.ProxyDescriptor import ProxyDescriptor
from ..proxy.proxy.not_visible.ProxyEntrypoint import ProxyEntrypoint, ProxyEntrypointParams
from ..source.AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ..source.AbstractSourceParams import AbstractSourceParams
from ..source.SourceDescriptor import SourceDescriptor
from ..adaptator.AdaptatorDescriptor import AdaptatorDescriptor
from ..interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
import json
from typing import Type, Any, Optional
import os
from ..interface.InterfaceDescriptor import InterfaceDescriptor
from ..source.SourceIndex import source_index
from ..adaptator.AdaptatorIndex import adaptator_index

class CRUDableEntityBuilder():
    """
    Enables you to build an entity type.
    """

    def __init__(self, crudable_source: Optional[AbstractCRUDableEntityType]):
        self.crudable_entity = crudable_source

    def get_built_entity(self) -> AbstractCRUDableEntityType:
        """
        Returns the constructed entity.
        """
        return ProxyEntrypoint.build(ProxyEntrypointParams(), self.crudable_entity)

    async def from_file(
        self, 
        file_path: str, 
        subs_index: dict[str, Any], 
        addon_source: dict[str, Type[AbstractCRUDableEntityTypeSource]], 
        addon_proxy: dict[str, Type[AbstractCRUDableEntityTypeProxy]]
    ):
        """
        Builds an entity type from a .json file that lists the source and proxies.

        :param file_path:
            The path to the .json file

        :param subs_index:
            An index that indicates the corresponding Python object for variables in descriptors.

        :param addon_source:
            An index of the library user's custom source modules.

        :param addon_proxy:
            An index of the library user's custom proxy modules.
        """
        index_ref = {}
        with open(file_path, "r") as f:
            for descriptor_dict in json.load(f):#on boucle sur les descriptor
                chain_start = self.crudable_entity is None#indique si c'est le premier descriptor que l'on rencontre
                if chain_start and "source" not in descriptor_dict:#on est au début de la chaine, et le descripteur n'indique aucune source : c'est donc lui la source
                    if descriptor_dict["name"] in source_index:#pure source
                        built_descriptor = (await SourceDescriptor(
                            **{
                                **descriptor_dict, 
                                "subs_index": subs_index,
                                "addons": addon_source
                            }
                        ).build().complete())
                    else:#adaptator
                        built_descriptor = (await AdaptatorDescriptor(
                            **{
                                **descriptor_dict, 
                                "subs_index": subs_index,
                                "addons": addon_source
                            }
                        ).build())#no complete, adaptator calls complete from source during build
                elif not chain_start and "source" in descriptor_dict:
                    raise Exception("On ne peut pas renseigner de source en milieu de chaîne")
                else:
                    descriptor = ProxyDescriptor(
                        **descriptor_dict, 
                        subs_index=subs_index,
                        addons=addon_proxy
                    )
                    if chain_start:
                        descriptor.base = subs_index[descriptor_dict["source"]]
                    else:
                        descriptor.base = self.crudable_entity
                    built_descriptor = descriptor.build()
                self.crudable_entity = built_descriptor
                if "ref" in descriptor_dict:#on place une référence sur l'entité jusqu'ici construite (permet de la référencer dans une autre fichier)
                    index_ref[descriptor_dict["ref"]] = self.crudable_entity
        return index_ref