from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ....Sentinel import Sentinel
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Fields import Fields
from ....Filter import FilterType, FilterInstance
from ...AbstractProxyParams import AbstractProxyParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools
from collections import defaultdict

class AllowedFilterOnField(BaseModel):
    field_name: str
    """
    The name of the field on which the user can filter.
    """

    allowed_filter_type: FilterType
    """
    The type of filter the user will be able to perform on this field.
    """

class FilterFirewallParams(AbstractProxyParams):
    """
    FilterFirewall proxy settings.
    """

    allowed_filter_on_fields: list[AllowedFilterOnField]
    """
    The list of filters that the CRUD user can fill in when reading.
    """
    
    @functools.cached_property
    def allowed_filter_type_index(self) -> dict[str, list[FilterType]]:
        """
        Index field_name->allowed_filter_type automatically created from allowed_filter_on_fields.
        """
        d = defaultdict(list)
        for o in self.allowed_filter_on_fields:
            d[o.field_name].append(o.allowed_filter_type)
        return dict(d)
    
class FilterFirewall(AbstractCRUDableEntityTypeProxy):
    """
    Whitelists filters that can be set by the CRUD user during the read.
    Modifies list_allowed_filter_type of fields in the interface.

    Example of descriptor, which allows a "contain" filter on "field_foo" and
    an "equal" filter on "field_bar":

    .. highlight:: json
    .. code-block:: json

        {
            "name": "FilterFirewall",
            "params": {
                "allowed_filter_on_fields": [
                    {
                        "field_name": "field_foo",
                        "allowed_filter_type": {
                            "filtration_type": "contain", 
                            "is_mandatory": false,
                            "default": null
                        }
                    },
                    {
                        "field_name": "field_bar",
                        "allowed_filter_type": {
                            "filtration_type": "equal", 
                            "is_mandatory": true,
                            "default": null
                        }
                    }
                ]
            }
        }

    """

    params: FilterFirewallParams
    """
    FilterFirewall proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: FilterFirewallParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.list_allowed_filter_type = params.allowed_filter_type_index.get(field.name, [])
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface
    
    #TODO : run a check_integration, to avoid blind data leaks

    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Does nothing for now.
        TODO: add validation.
        """
        #TODO : validation ?
        """for filter_instance in list_filter_instance:
            assert filter_instance.field_name in self.allowed_filter_type_index#TODO : meilleur gestion de l'erreur
            assert filter_instance.filtration_type == self.allowed_filter_type_index[filter_instance.field_name].filtration_type
            assert not self.allowed_filter_type_index[filter_instance.field_name].is_mandatory or filter_instance.filter_value is not None"""
        return await self.base.read(params)
