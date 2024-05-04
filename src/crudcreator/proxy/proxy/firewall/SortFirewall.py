from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ....Sentinel import Sentinel
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Fields import Fields
from ....Sort import SortType
from ...AbstractProxyParams import AbstractProxyParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools
from collections import defaultdict

class AllowedSortOnField(BaseModel):
    field_name: str
    """
    The name of the field on which the user can sort.
    """

    allowed_sort_type: SortType
    """
    The type of sort the user will be able to perform on this field.
    """

class SortFirewallParams(AbstractProxyParams):
    """
    SortFirewallParams proxy settings.
    """

    allowed_sort_on_fields: list[AllowedSortOnField]
    """
    The list of sorts that the CRUD user can fill in when reading.
    """
    
    @functools.cached_property
    def allowed_sort_type_index(self) -> dict[str, list[SortType]]:
        """
        Index field_name->allowed_filter_type automatically created from allowed_sort_on_fields.
        """
        d = defaultdict(list)
        for o in self.allowed_sort_on_fields:
            d[o.field_name].append(o.allowed_sort_type)
        return dict(d)
    
class SortFirewall(AbstractCRUDableEntityTypeProxy):
    """
    Whitelists sorts that can be set by the CRUD user during the read.
    Modifies list_allowed_sort_type of fields in the interface.

    #TODO : example

    """

    params: SortFirewallParams
    """
    SortFirewall proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: SortFirewallParams) -> CRUDableEntityTypeInterface:
        list_new_field = []
        for field in base_interface.fields.list_field:
            field = field.model_copy()
            field.list_allowed_sort_type = params.allowed_sort_on_fields.get(field.name, [])
            list_new_field.append(field)
        base_interface.fields = Fields.build(list_new_field)
        return base_interface
    
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
