from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ....Sentinel import Sentinel
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Fields import Fields
from ....Filter import FilterInstance
from enum import Enum
from ....Link import Link
from ....LinkType import LinkType, Cardinality
from sqlalchemy.sql import Select, Delete, Insert, Update
from ...AbstractProxyParams import AbstractProxyParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....transaction.AbstractTransaction import AbstractTransaction
import functools

class LinkedField(BaseModel):
    field_name: str
    """
    The name of the current entity type's field to which the link is made.
    """

    link: Link
    """
    The link.
    """

class CreateLinkParams(AbstractProxyParams):
    """
    CreateLink proxy settings.
    """

    list_linked_field : list[LinkedField]
    """
    List of links.
    """

    interface_merge: bool
    """
    Does nothing.
    TODO ?
    """
    
    @functools.cached_property
    def link_index(self) -> dict[str, str]:
        """
        A field_name->link index built automatically from list_linked_field.
        """
        return {l.field_name:l.link for l in self.list_linked_field}

    
class CreateLink(AbstractCRUDableEntityTypeProxy):
    """
    Creates a link with another entity type.
    Only change the interface of the current entity type.
    Does not change any CRUD actions.
    Must therefore be used with other proxies, which will implement a way of handling these links
    (for example, CascadeDelete or CascadeCreateAndUpdate proxies).

    Example of a descriptor linking the current entity with the "entity_bis" entity on the "field_to_join" and
    "field_to_be_joined", in one-to-one mode:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "CreateLink",
            "params": {
                "interface_merge": true,
                "list_linked_field": [
                    {
                        "field_name": "field_to_join",
                        "link": {
                            "entity_type_linked_to": "$entity_bis$",
                            "field_name_linked_to": "field_to_be_joined",
                            "type": {
                                "source": {
                                    "min": "one",
                                    "max": "one"
                                },
                                "dest": {
                                    "min": "one",
                                    "max": "one"
                                }
                            }
                        }
                    }
                ]
            }
        }
    """

    params: CreateLinkParams
    """
    CreateLink proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: CreateLinkParams) -> CRUDableEntityTypeInterface:
        new_list_field = []
        for field in base_interface.fields.list_field:
            new_field = field.model_copy()
            if field.name not in params.link_index:
                new_list_field.append(new_field)
            else:
                #if params.link_index[field.name].type.dest.max == Cardinality.one:
                new_field.link = params.link_index[field.name]
                new_list_field.append(new_field)
                """if params.interface_merge:
                    for linked_field in params.link_index[field.name].entity_type_linked_to.interface.fields.list_field:
                        if linked_field.name != params.link_index[field.name].field_name_linked_to:
                            new_field = linked_field.model_copy()
                            #new_field.can_be_created = False#TODO ? faire un writable firewall
                            new_field.is_id_field = False#?
                            new_list_field.append(new_field)"""
                #else:
                #    raise NotImplementedError()
        base_interface.fields = Fields.build(new_list_field)
        return base_interface
    

    
    