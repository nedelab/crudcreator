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

class UpdateFirewallParams(AbstractProxyParams):
    """
    UpdateFirewall proxy settings.
    """

    list_updatable_field_name: list[str]
    """
    The list of field names that the CRUD user can fill in when updating an entity.
    """

    @functools.cached_property
    def index_updatable_field_name(self) -> dict[str, bool]:
        """
        Index on field names. Automatically created from list_updatable_field_name.
        """
        return {k:True for k in self.list_updatable_field_name}

        
class UpdateFirewall(AbstractCRUDableEntityTypeProxy):

    """
    Whitelists the fields that can be filled in when an entity is updated by the CRUD user.
    Set can_be_updated to False for other interface fields.

    Example of descriptor, which allows only the "field_foo" and "field_bar" fields to be filled at update:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "UpdateFirewall",
            "params": {
                "list_updatable_field_name": [
                    "field_foo",
                    "field_bar"
                ]
            }
        }
    """

    params: UpdateFirewallParams
    """
    UpdateFirewall proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: UpdateFirewallParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.can_be_updated = field.name in params.index_updatable_field_name
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface
    
    async def update(self, params: UpdateParams) -> list[dict[str, Any]]:
        """
        Checks that the fields entered in the CRUD request are part of the whitelist.
        """
        for field_name in params.dict_updator_value:
            assert field_name in self.params.index_updatable_field_name
        return await self.base.update(params)
    
    