from typing import Any
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy, AbstractProxyParams
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from ....Sort import FieldToSort

class AddSortParams(AbstractProxyParams):
    """
    AddSort proxy parameters.
    """
    
    list_field_on_which_to_sort: list[FieldToSort]
    """
    The list of sorts to add to the CRUD request.
    """

class AddSort(AbstractCRUDableEntityTypeProxy):
    """
    Adds hard-coded "sort" to the read CRUD request. 

    .. warning::

        Does not perform a sort here, but adds the sort to the request
        (so that it can be processed later by the source adaptator)

    Example of a descriptor, which will return a list of entities, sorted by
    field_foo in ascending order and then field_bar by descending order (lexicographic order).

    .. highlight:: json
    .. code-block:: json

        {
            "name": "AddSort",
            "params": {
                "list_field_on_which_to_sort": [
                    {
                        "field_name": "field_foo",
                        "type": "asc"
                    },
                    {
                        "field_name": "field_bar",
                        "type": "desc"
                    }
                ]
            }
        }
    """
    
    params: AddSortParams
    """
    AddSort proxy parameters.
    """
        
    async def read(self, params: ReadParams) -> list[Any]:
        """
        Adds the list of sort instances to the CRUD request, then forwards the request to the next proxy.
        """
        return await self.base.read(
            ReadParams(
                transaction=params.transaction, 
                list_filter_instance=params.list_filter_instance, 
                list_read_field=params.list_read_field,
                dict_read_options=params.dict_read_options,
                limit=params.limit,
                offset=params.offset,
                must_read_distinct=params.must_read_distinct,
                list_field_on_which_to_sort=params.list_field_on_which_to_sort+self.params.list_field_on_which_to_sort,
            )
        )