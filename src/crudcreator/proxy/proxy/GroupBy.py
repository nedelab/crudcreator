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

class GroupByParams(AbstractProxyParams):
    """
    GroupBy proxy settings.
    """

    grouped_by_fields: list[str]
    """
    Names of fields to be grouped by.
    """

    group_name: str
    """
    The name of the list that will contain all the other fields.
    """

    one_elem_with_all_none_means_empty: bool
    """
    If there is only one element in the list, and all the attributes of this element are set to None,
    then the list is considered empty. (to manage outer joins)
    """

    see_group_only_on_option: Optional[str] = None
    """
    The name of the option which, if set to "True", displays the group in the entities read.
    """
    
    @functools.cached_property
    def index_grouped_by_fields(self) -> dict[str, bool]:
        """
        Index on grouped by field names. Automatically created from grouped_by_fields.
        """
        return {k:True for k in self.grouped_by_fields}
    
class GroupBy(AbstractCRUDableEntityTypeProxy):
    """
    Has more or less the same effect as a SQL "group by" accompanied by a "GROUP_CONCAT".
    Groups entities by distinct values of fields appearing in grouped_by_fields, and groups all entities 
    with these values in a list.
    
    Not to be confused with the "GatherField" proxy.
    
    Example of descriptor. Group by field_foo and field_bar, and collects the list of entities in the "my_group" field:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "GroupBy",
            "params": {
                "group_name": "my_group",
                "grouped_by_fields": ["field_foo", "field_bar"],
                "one_elem_with_all_none_means_empty": true,
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
                "field_foo": "1",
                "field_bar": "1",
                "my_group": [
                    {
                        "other_field": "a",
                        "other_field_2": "b"
                    },
                    {
                        "other_field": "c",
                        "other_field_2": "d"
                    }
                ]
            },
            {
                "field_foo": "1",
                "field_bar": "2",
                "my_group": [
                    {
                        "other_field": "a",
                        "other_field_2": "b"
                    }
                ]
            }
        ]

    """

    params: GroupByParams
    """
    GroupBy proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: GroupByParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            if field.name in params.index_grouped_by_fields:
                list_new_field.append(field.model_copy())
        group_field = FieldOfCRUDableEntityType(
                name=params.group_name,
                type=list[
                    base_interface.get_sub_interface(
                        f"{base_interface.name}_{params.group_name}", 
                        [field_name for field_name in base_interface.fields.index_field_by_name if field_name not in params.index_grouped_by_fields]
                    ).get_read_response_data_model()
                ],
                list_allowed_filter_type=[],#you can't filter on a list, but on attributes (place this module after a filterfirewall)
                can_be_created=False,#can't write a list
                can_be_updated=False,#can't write a list
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

        #start by creating the request to be passed on to the next proxy (unfold the list)
        new_list_read_field = params.list_read_field.copy()
        if self.params.group_name in new_list_read_field:
            new_list_read_field.remove(self.params.group_name)
            new_list_read_field = new_list_read_field+[
                field.name 
                for field in self.base.interface.fields.list_field 
                if field.name not in self.params.grouped_by_fields and 
                field.can_be_read
            ]
        params.list_read_field = new_list_read_field
        list_row = await self.base.read(params)

        #group the result as required
        dict_group = defaultdict(list)
        if not see_group:
            return [
                {
                    **{
                        k:v 
                        for k,v in row.items()
                        if k in self.params.index_grouped_by_fields
                    },
                    self.params.group_name: None
                }
                for row in list_row
            ]#TODO : bug, uniqueness of grouped by fields ?
        else:
            for row in list_row:
                k = tuple(row[field_name] for field_name in self.params.index_grouped_by_fields)
                dict_group[k].append({field_name:row[field_name] for field_name in row if field_name not in self.params.index_grouped_by_fields})
            dict_group = dict(dict_group)
            return [
                {
                    **{
                        self.params.grouped_by_fields[i]:k[i]
                        for i in range(0, len(self.params.grouped_by_fields))
                    }, 
                    **{self.params.group_name: (
                        []
                        if (
                            self.params.one_elem_with_all_none_means_empty and
                            len(dict_group[k]) == 1 and
                            all([v is None for _,v in dict_group[k][0].items()])
                        )
                        else
                        dict_group[k]
                    )}
                }
                for k in dict_group
            ]
