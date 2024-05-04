from typing import Any
from pydantic import BaseModel, create_model, field_validator
from typing import Optional
from ...Sentinel import Sentinel
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from...AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ...FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ...Fields import Fields
from ...Filter import FilterInstance
from ..AbstractProxyParams import AbstractProxyParams
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools

class Translation(BaseModel):
    
    source: str
    """
    Source-side field name.
    """

    destination: str
    """
    Destination-side field name.
    """

class RenameParams(AbstractProxyParams):
    """
    Rename proxy settings.
    """

    translation_list : list[Translation]
    """
    List of changes to be made.
    """

    interface_name: str
    """
    Destination-side entity name.
    """

    @field_validator("translation_list")
    def unique_value(cls, translation_list: list[Translation]) -> list[Translation]:
        """
        Checks that each field has a unique name, both on the source and destination sides.
        """
        list_source = [t.source for t in translation_list]
        list_interface = [t.destination for t in translation_list]
        if len(list_source) > len(set(list_source)):
            raise ValueError("Some source-side values are not unique")
        if len(list_interface) > len(set(list_interface)):
            raise ValueError("Some destination-side values are not unique")
        return translation_list
    
    @functools.cached_property
    def source_to_destination_index(self) -> dict[str, str]:
        """
        A source->destination index built automatically from translation_list.
        """
        return {t.source:t.destination for t in self.translation_list}
    
    @functools.cached_property
    def destination_to_source_index(self) -> dict[str, str]:
        """
        A destination->source index built automatically from translation_list.
        """
        return {t.destination:t.source for t in self.translation_list}

        
class Rename(AbstractCRUDableEntityTypeProxy):
    """
    Proxy that changes entity field names.
    Also changes the entity name.

    Example of descriptor, which changes the name of the interface on the destination side to "my_entity",
    and the field name "column_1" to "field_1" on the destination side:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "Rename",
            "params": {
                "interface_name": "my_entity",
                "translation_list": [
                    {
                        "source": "column_1",
                        "destination": "field_1"
                    }
                ]
            }
        }

    """

    params: RenameParams
    """
    Rename proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: RenameParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.name = params.source_to_destination_index.get(field.name, field.name)
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        base_interface.name = params.interface_name
        return base_interface
    
    def _change_name(self, dict_key_index: dict[str, str], old_name: str) -> str:
        if old_name in dict_key_index:
            return dict_key_index[old_name]
        else:
            return old_name
        
    def _change_key(self, dict_key_index: dict[str, str], dict_value: dict[str, Any]) -> dict[str, Any]:
        dict_renamed_value = {}
        for k, v in dict_value.items():
            dict_renamed_value[self._change_name(dict_key_index, k)] = v
        return dict_renamed_value

    
    def _rename_source_to_destination(self, old_name: str) -> str:
        return self._change_name(self.params.source_to_destination_index, old_name)
    
    def _rename_destination_to_source(self, old_name: str) -> str:
        return self._change_name(self.params.destination_to_source_index, old_name)
    
    def _rename_dict_destination_to_source(self, dict_value: dict[str, Any]) -> dict[str, Any]:
        return self._change_key(self.params.destination_to_source_index, dict_value)
    
    def _rename_dict_source_to_destination(self, dict_value: dict[str, Any]) -> dict[str, Any]:
        return self._change_key(self.params.source_to_destination_index, dict_value)
    
    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Changes filter names from destination to source.
        Changes the name of columns to be read from destination to source.
        Calls the next proxy.
        Then changes the name of the result columns from source to destination.
        """
        new_list_filter_instance = []
        for filter_instance in params.list_filter_instance:
            new_filter_instance = filter_instance.model_copy()
            new_filter_instance.field_name = self._rename_destination_to_source(filter_instance.field_name)
            new_list_filter_instance.append(new_filter_instance)
        new_list_read_field = []
        for field_name in params.list_read_field:
            new_list_read_field.append(self._rename_destination_to_source(field_name))
        return [
            self._rename_dict_source_to_destination(row)
            for row in await self.base.read(
                ReadParams(
                    transaction=params.transaction,
                    list_filter_instance=new_list_filter_instance,
                    list_read_field=new_list_read_field,
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
        Change column names from destination to source, then call the next proxy.
        """
        return await self.base.create(
                CreateParams(
                    transaction=params.transaction,
                    dict_creator_value=self._rename_dict_destination_to_source(params.dict_creator_value),
                    dict_creator_options=params.dict_creator_options
                )
            )
    
    async def delete(self, params: DeleteParams):
        """
        Change ids from destination to source, then call the next proxy.
        """
        return await self.base.delete(
                DeleteParams(
                    transaction=params.transaction,
                    dict_deletor_value=self._rename_dict_destination_to_source(params.dict_deletor_value),
                    dict_deletor_options=params.dict_deletor_options
                )  
            )
    
    async def update(self, params: UpdateParams):
        """
        Changes column names and ids from destination to source, then calls the next proxy.
        """
        return await self.base.update(
                UpdateParams(
                    transaction=params.transaction,
                    dict_ids=self._rename_dict_destination_to_source(params.dict_ids),
                    dict_updator_value=self._rename_dict_destination_to_source(params.dict_updator_value),
                    dict_updator_options=params.dict_updator_options
                )
            )

    