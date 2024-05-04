from typing import Any
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....Filter import FilterInstance
from ...AbstractProxyParams import AbstractProxyParams
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface

class ReadDistinctFirewallParams(AbstractProxyParams):
    """
    ReadDistinctFirewall proxy parameters.
    """

    can_indicate_read_distinct: bool
    """
    Can the user specify that only entities with a distinct value are to be read?
    """
    
    
class ReadDistinctFirewall(AbstractCRUDableEntityTypeProxy):
    """
    Enable or disable the user's right to specify that only entities with a distinct value should be read.
    Modifies the interface.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "ReadDistinctFirewall",
            "params": {
                "can_indicate_read_distinct": false
            }
        }

    """
    
    params: ReadDistinctFirewallParams
    """
    ReadDistinctFirewall proxy parameters.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: ReadDistinctFirewallParams) -> CRUDableEntityTypeInterface:
        base_interface.can_indicate_read_distinct = params.can_indicate_read_distinct
        return base_interface


    