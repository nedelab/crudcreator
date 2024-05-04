from typing import Any
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....Filter import FilterInstance
from ...AbstractProxyParams import AbstractProxyParams
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface

class ReadDistinctParams(AbstractProxyParams):
    """
    ReadDistinct proxy parameters.
    Nothing.
    """
    pass
    
    
class ReadDistinct(AbstractCRUDableEntityTypeProxy):
    """
    Makes the request return only entities with distinct read values.
    Modifies the interface so that the user can no longer set "must_read_distinct" himself.

    .. warning::

        Does not perform a "distinct" operation here, but adds the "must_read_distinct" parameters to the request
        (so that it can be processed later by the source adaptator)

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "ReadDistinct",
            "params": {}
        }

    """
    
    params: ReadDistinctParams
    """
    ReadDistinct proxy parameters.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: ReadDistinctParams) -> CRUDableEntityTypeInterface:
        base_interface.can_indicate_read_distinct = False
        return base_interface

    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Adds the "must_read_distinct" parameters to the request.
        """
        return await self.base.read(
            ReadParams(
                transaction=params.transaction, 
                list_filter_instance=params.list_filter_instance, 
                list_read_field=params.list_read_field,
                dict_read_options=params.dict_read_options,
                limit=params.limit,
                offset=params.offset,
                must_read_distinct=True,
                list_field_on_which_to_sort=params.list_field_on_which_to_sort,
            )
        )

    