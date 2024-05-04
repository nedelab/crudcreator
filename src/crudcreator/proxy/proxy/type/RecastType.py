from typing import Any, Callable
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from pydantic import BaseModel
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....Fields import Fields
from ....Filter import FilterInstance
import logging
from .SpecialType import SpecialType
from ...AbstractProxyParams import AbstractProxyParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools

class FieldRecast(BaseModel):
    field_name: str
    """
    The name of the field to be recast.
    """

    special_type: SpecialType
    """
    The new type.
    """

class RecastTypeParams(AbstractProxyParams):
    """
    RecastType proxy settings.
    """

    list_recast_field : list[FieldRecast]
    """
    List of recasts to do.
    """

    @functools.cached_property
    def recast_index(self) -> dict[str, SpecialType]:
        """
        A field_name->special_type index built automatically from list_recast_field.
        """
        return {r.field_name:r.special_type for r in self.list_recast_field}


class RecastType(AbstractCRUDableEntityTypeProxy):
    """
    Changes the type of a field and reprocesses it to match the new type.

    Example of descriptor, which changes the type of the "field_bool_converted" field, which is a str at source,
    and becomes a boolean at destination.

    .. highlight:: json
    .. code-block:: json

        {
            "name": "RecastType",
            "params": {
                "list_recast_field": [
                    {
                        "field_name": "field_bool_converted",
                        "special_type": "$oui_non_type$"
                    }
                ]
            }
        }

    With "yes_no_type" defined as follows:

    .. highlight:: python
    .. code-block:: python

        def oui_non_to_bool(v: str):
            if v == "oui":
                return True
            elif v == "non":
                return False
            elif v == None:
                return None
            else:
                raise NotImplementedError()
            
        def bool_to_oui_non(v: bool):
            if v == True:
                return "oui"
            elif v == False:
                return "non"
            elif v == None:
                return None
            else:
                raise NotImplementedError() 
                
        oui_non_type = SpecialType(
            destination_type=bool,
            destination_to_source=bool_to_oui_non,
            source_to_destination=oui_non_to_bool
        )

    Let's assume that the source contains the following entities:

    .. highlight:: json
    .. code-block:: json

        [
            {
                "field_foo": "1",
                "field_bar": "1",
                "field_bool_converted": "oui"
            },
            {
                "field_foo": "1",
                "field_bar": "1",
                "field_bool_converted": "non"
            },
            {
                "field_foo": "1",
                "field_bar": "2",
                "field_bool_converted": null
            }
        ]

    A read will therefore return a result of this form :

    .. highlight:: json
    .. code-block:: json

        [
            {
                "field_foo": "1",
                "field_bar": "1",
                "field_bool_converted": true
            },
            {
                "field_foo": "1",
                "field_bar": "1",
                "field_bool_converted": false
            },
            {
                "field_foo": "1",
                "field_bar": "2",
                "field_bool_converted": null
            }
        ]

    And the entity type interface will be changed accordingly (field_bool_converted will be of type bool).

    The recast is also applied on the filters, the creation body, the update body and ids, and the delete ids.
    """

    params: RecastTypeParams
    """
    RecastType proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: RecastTypeParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field.model_copy()
            if field.name in params.recast_index:
                field.default = params.recast_index[field.name].source_to_destination(field.default)
                field.type = params.recast_index[field.name].destination_type
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        """ TODO : faire des vérifications de compatibilité avec l'interface de la base
        index_base = base.get_fields().index_field_by_name
        for field_name in recast_index:
            if field_name not in index_base:
                logging.warning(f"Reprocess : le champ {field_name} n'existe pas")
        """
        return base_interface
    
    def _reprocess_source_to_destination(self, field_name: str, v: Any) -> Any:
        reprocess = self.params.recast_index.get(field_name, None)
        if reprocess is None:
            return v
        else:
            return reprocess.source_to_destination(v)
        
    def _reprocess_destination_to_source(self, field_name: str, v: Any) -> Any:
        reprocess = self.params.recast_index.get(field_name, None)
        if reprocess is None:
            return v
        else:
            return reprocess.destination_to_source(v)
        
    async def read(self, params: ReadParams) -> list[Any]:
        """
        Recast filters from destination type to source type.
        Sends the query to the next proxy.
        Then recasts the result fields from the source type to the destination type, before returning the result.
        """
        new_list_filter_instance = []
        for filter_instance in params.list_filter_instance:
            new_filter_instance = filter_instance.model_copy()
            new_filter_instance.filter_value = self._reprocess_destination_to_source(
                filter_instance.field_name, 
                filter_instance.filter_value
            )
            new_list_filter_instance.append(new_filter_instance)
        return [
            {
                k:self._reprocess_source_to_destination(k, v)
                for k,v in dict_value_base.items()
            }
            for dict_value_base in await self.base.read(
                ReadParams(
                    transaction=params.transaction,
                    list_filter_instance=new_list_filter_instance,
                    list_read_field=params.list_read_field,
                    dict_read_options=params.dict_read_options,
                    limit=params.limit,
                    offset=params.offset,
                    must_read_distinct=params.must_read_distinct,
                    list_field_on_which_to_sort=params.list_field_on_which_to_sort,
                )
            )
        ]
    
    async def create(self, params: CreateParams):
        """
        Recast fields from destination type to source type.
        Then sends the query to the next proxy.
        """
        return await self.base.create(
            CreateParams(
                transaction=params.transaction,
                dict_creator_value={
                    k:self._reprocess_destination_to_source(k, v)
                    for k,v in params.dict_creator_value.items()
                },
                dict_creator_options=params.dict_creator_options
            )
        )
    
    async def delete(self, params: DeleteParams):
        """
        Recast id fields from destination type to source type.
        Then sends the query to the next proxy.
        """
        return await self.base.delete(
            DeleteParams(
                transaction=params.transaction,
                dict_deletor_value={
                    k:self._reprocess_destination_to_source(k, v)
                    for k,v in params.dict_deletor_value.items()
                },
                dict_deletor_options=params.dict_deletor_options
            )
        )
    
    async def update(self, params: UpdateParams):
        """
        Recast update fields and id fields from destination type to source type.
        Then sends the query to the next proxy.
        """
        return await self.base.update(
            UpdateParams(
                transaction=params.transaction,
                dict_ids={
                    k:self._reprocess_destination_to_source(k, v)
                    for k,v in params.dict_ids.items()
                }, 
                dict_updator_value={
                    k:self._reprocess_destination_to_source(k, v)
                    for k,v in params.dict_updator_value.items()
                },
                dict_updator_options=params.dict_updator_options
            )
        )

    