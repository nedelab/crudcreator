from typing import Any
from pydantic import BaseModel, create_model, validator
from typing import Optional
from ....Sentinel import Sentinel
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Fields import Fields
from ....Filter import FilterInstance
from ...AbstractProxyParams import AbstractProxyParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools

class IdFirewallParams(AbstractProxyParams):
    """
    IdFirewall proxy settings.
    """

    list_id_field_name: list[str]
    """
    List of field names that the CRUD user can use as ids.
    """

    @functools.cached_property
    def index_id_field_name(self) -> dict[str, bool]:
        """
        Index on field names. Automatically created from list_id_field_name.
        """
        return {k:True for k in self.list_id_field_name}

        
class IdFirewall(AbstractCRUDableEntityTypeProxy):
    """
    Whitelists the fields that can be used as ids by the CRUD user.
    Set is_id_field to False for other interface fields.

    Example of descriptor, which makes only the "field_foo" and "field_bar" fields usable as ids:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "IdFirewall",
            "params": {
                "list_id_field_name": [
                    "field_foo",
                    "field_bar"
                ]
            }
        }
    """

    params: IdFirewallParams
    """
    IdFirewall proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: IdFirewallParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.is_id_field = field.name in params.index_id_field_name
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface

    async def update(self, params: UpdateParams) -> list[dict[str, Any]]:
        """
        Checks that the fields used as ids, given in the CRUD request, are indeed part of the whitelist.
        """
        for field_name in params.dict_ids:
            assert field_name in self.params.index_id_field_name#TODO : can do better
        return await self.base.update(params)
    
    async def delete(self, params: DeleteParams):
        """
        Checks that the fields used as ids, given in the CRUD request, are indeed part of the whitelist.
        """
        for field_name in params.dict_deletor_value:
            assert field_name in self.params.index_id_field_name#TODO : can do better
        return await self.base.delete(params)
    
    