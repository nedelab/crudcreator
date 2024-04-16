from typing import Any
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ...Filter import FilterInstance
from ..AbstractProxyParams import AbstractProxyParams
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from collections import defaultdict
import functools
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ...Fields import Fields, FieldOfCRUDableEntityType
from typing import Optional

class GatherFieldsParams(AbstractProxyParams):
    """
    GatherFields proxy settings.
    """

    gathered_fields: list[str]
    """
    The list of field names to be collected in the group.
    """

    group_name: str
    """
    The name to give to the new group.
    """

    see_group_only_on_option: Optional[str] = None
    """
    The name of the option which, if set to "True", displays the group in the entities read.
    """
    
    @functools.cached_property
    def index_gathered_fields(self) -> dict[str, bool]:
        """
        Index on grouped field names. Automatically created from gathered_fields.
        """
        return {k:True for k in self.gathered_fields}
    
class GatherFields(AbstractCRUDableEntityTypeProxy):
    """
    Groups several fields from the same entity into a single object field.
    Not a "group by" as understood in SQL.
    The group will therefore be an object and not a list.
    Not to be confused with the "GroupBy" proxy.

    Example of descriptor. Gathers field_foo and field_bar into a single field named "my_group"

    .. highlight:: json
    .. code-block:: json

        {
            "name": "GatherFields",
            "params": {
                "group_name": "my_group",
                "gathered_fields": ["field_foo", "field_bar"],
                "see_group_only_on_option": "extend_group"
            }
        }

    Let's assume that the source contains the following entities:

    .. highlight:: json
    .. code-block:: json

        [
            {
                "field_foo": "1",
                "field_bar": "1",
                "other_field": "a",
                "other_field_2": "b"
            },
            {
                "field_foo": "1",
                "field_bar": "1",
                "other_field": "c",
                "other_field_2": "d"
            },
            {
                "field_foo": "1",
                "field_bar": "2",
                "other_field": "a",
                "other_field_2": "b"
            }
        ]

    A read will therefore return a result of this form :

    .. highlight:: json
    .. code-block:: json

        [
            {
                "other_field": "a",
                "other_field_2": "b",
                "my_group": [
                    {
                        "field_foo": "1",
                        "field_bar": "1"
                    }
                ]
            },
            {
                "other_field": "c",
                "other_field_2": "d",
                "my_group": [
                    {
                        "field_foo": "1",
                        "field_bar": "1"
                    }
                ]
            },
            {
                "other_field": "a",
                "other_field_2": "b"
                "my_group": [
                    {
                        "field_foo": "1",
                        "field_bar": "2"
                    }
                ]
            }
        ]
    """
    
    params: GatherFieldsParams
    """
    GatherFields proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: GatherFieldsParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            if field.name not in params.index_gathered_fields:
                list_new_field.append(field.model_copy())
        group_field = FieldOfCRUDableEntityType(
                name=params.group_name,
                type=(
                    base_interface.get_sub_interface(
                        params.group_name, 
                        [field_name for field_name in base_interface.fields.index_field_by_name if field_name in params.index_gathered_fields]
                    ).get_read_response_data_model()
                ),
                list_allowed_filter_type=[],#you can't filter on an object, but on attributes (place this module after a filterfirewall)
                can_be_created=False,#cannot write an object
                can_be_updated=False,#cannot write an object
                is_id_field=False
            )
        if params.see_group_only_on_option is not None:
            group_field.type = Optional[group_field.type]
        list_new_field.append(group_field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface

    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Builds the list of fields to be read, depending on whether the option is enabled.
        Sends the request to the next proxy.
        Then groups the entities as required, before returning the result.
        """
        see_group = (
            self.params.see_group_only_on_option is not None and 
            params.dict_read_options.get(self.params.see_group_only_on_option, False) == True
        )
        new_list_read_field = params.list_read_field.copy()
        if self.params.group_name in new_list_read_field:
            new_list_read_field.remove(self.params.group_name)
            new_list_read_field = new_list_read_field+[
                field.name 
                for field in self.base.interface.fields.list_field 
                if field.name in self.params.index_gathered_fields and 
                field.can_be_read
            ]
        params.list_read_field = new_list_read_field
        list_row = await self.base.read(params)
        return [
            {
                **{
                    k:v
                    for k,v in row.items()
                    if k not in self.params.index_gathered_fields
                }, 
                **{self.params.group_name: (
                    None if not see_group else
                    {
                        k:row[k]
                        for k in self.params.index_gathered_fields
                    }
                )}
            }
            for row in list_row
        ]
