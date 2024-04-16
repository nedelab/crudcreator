from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ...Sentinel import Sentinel
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from...AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ...FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ...Fields import Fields
from ...Filter import FilterType, FilterInstance
from ..AbstractProxyParams import AbstractProxyParams
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools
from collections import defaultdict

class DefaultOnField(BaseModel):
    field_name: str
    """
    The name of the field to which to give the default value.
    """

    default: Any
    """
    The default value.
    """

class AddDefaultParams(AbstractProxyParams):
    """
    AddDefault proxy settings.
    """

    default_on_fields: list[DefaultOnField]
    """
    List of default fields/values to be given.
    """
    #TODO : check that "field_name" is unique

    @functools.cached_property
    def default_index(self) -> dict[str, list[FilterType]]:
        """
        Index field_name->default automatically created from default_on_fields.
        """
        return {o.field_name:o.default for o in self.default_on_fields}
    
class AddDefault(AbstractCRUDableEntityTypeProxy):
    """
    Adds default values to certain fields.
    
    Example of descriptor, which will add the default value of 10 to the "field_foo" field:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "AddDefault",
            "params": {
                "default_on_fields": [
                    {
                        "field_name": "field_foo",
                        "default": 10
                    }
                ]
            }
        }
    """

    params: AddDefaultParams
    """
    AddDefault proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: AddDefaultParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.default = params.default_index.get(field.name, field.default)
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface
    
    #TODO : actually add default (because for now, fastapi does it all by itself)