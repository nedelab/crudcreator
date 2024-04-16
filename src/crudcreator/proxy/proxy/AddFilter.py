from typing import Any
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ...Filter import FilterInstance
from ..AbstractProxyParams import AbstractProxyParams
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams

class AddFilterParams(AbstractProxyParams):
    """
    AddFilter proxy parameters.
    """
    
    list_filter_instance_to_add: list[FilterInstance]
    """
    The list of filter instances to be added.
    """
    
    
class AddFilter(AbstractCRUDableEntityTypeProxy):
    """
    Adds hard-coded filter instances to the read CRUD request.

    Example of descriptor, which will return, to the user executing a read,
    only those entities whose "can_be_seen" field is set to True:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "AddFilter",
            "params": {
                "list_filter_instance_to_add": [
                    {
                    "field_name": "can_be_seen",
                    "filter_value": true,
                    "filtration_type": "equal"
                    }
                ]
            }
        }

    """
    
    params: AddFilterParams
    """
    AddFilter proxy parameters.
    """

    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Adds the list of filter instances to the CRUD request, then forwards the request to the next proxy.
        """
        return await self.base.read(
            ReadParams(
                transaction=params.transaction, 
                list_filter_instance=params.list_filter_instance+self.params.list_filter_instance_to_add, 
                list_read_field=params.list_read_field,
                dict_read_options=params.dict_read_options
            )
        )

    