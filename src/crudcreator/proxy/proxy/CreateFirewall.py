from typing import Any
from pydantic import BaseModel, create_model, validator
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

class CreateFirewallParams(AbstractProxyParams):
    """
    CreateFirewall proxy settings.
    """
    
    list_creatable_field_name: list[str]
    """
    The list of field names that the CRUD user can fill in when creating an entity.
    """

    @functools.cached_property
    def index_creatable_field_name(self) -> dict[str, bool]:
        """
        Index on field names. Automatically created from list_creatable_field_name.
        """
        return {k:True for k in self.list_creatable_field_name}

        
class CreateFirewall(AbstractCRUDableEntityTypeProxy):
    """
    Whitelists the fields that can be filled in when an entity is created by the CRUD user.
    Set can_be_created to False for other interface fields.

    Example of descriptor, which allows only the "field_foo" and "field_bar" fields to be filled at creation:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "CreateFirewall",
            "params": {
                "list_creatable_field_name": [
                    "field_foo",
                    "field_bar"
                ]
            }
        }
    """

    params: CreateFirewallParams
    """
    CreateFirewall proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: CreateFirewallParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.can_be_created = field.name in params.index_creatable_field_name
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface
    
    async def create(self, params: CreateParams) -> list[dict[str, Any]]:
        """
        Checks that the fields entered in the CRUD request are part of the whitelist.
        """
        for field_name in params.dict_creator_value:
            assert field_name in self.params.index_creatable_field_name
        return await self.base.create(params)
    
    