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

class ReadFirewallParams(AbstractProxyParams):
    """
    ReadFirewall proxy settings.
    """

    list_readable_field_name: list[str]
    """
    List of field names that the CRUD user can read.
    """

    @functools.cached_property
    def index_readable_field_name(self) -> dict[str, bool]:
        """
        Index on field names. Automatically created from list_readable_field_name.
        """
        return {k:True for k in self.list_readable_field_name}

        
class ReadFirewall(AbstractCRUDableEntityTypeProxy):
    """
    Whitelists the fields that can be read by the CRUD user.
    Set can_be_read to False for other interface fields.

    Example of descriptor, which makes only the "field_foo" and "field_bar" fields visible for reading:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "ReadFirewall",
            "params": {
                "list_readable_field_name": [
                    "field_foo",
                    "field_bar"
                ]
            }
        }
    """

    params: ReadFirewallParams
    """
    ReadFirewall proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: ReadFirewallParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.can_be_read = field.name in params.index_readable_field_name
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface
    
    #TODO : assert in check_integrity to avoid blind data leakage?

    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Checks that the fields to be read, given in the CRUD request, are indeed part of the whitelist.
        """
        for field_name in params.list_read_field:
            assert field_name in self.params.index_readable_field_name#TODO : can do better
        return await self.base.read(params)
    
    