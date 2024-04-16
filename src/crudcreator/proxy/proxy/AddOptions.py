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
from ...OptionModel import OptionModel
import copy

class AddOptionsParams(AbstractProxyParams):
    """
    AddOptions proxy settings.
    """

    list_read_options: list[OptionModel] = []
    """
    The list of options that will be requested from the CRUD user for the read.
    """

    list_creator_options: list[OptionModel] = []
    """
    The list of options that will be requested from the CRUD user for create.
    """

    list_updator_options: list[OptionModel] = []
    """
    The list of options that will be requested from the CRUD user for the update.
    """

    list_deletor_options: list[OptionModel] = []
    """
    The list of options the CRUD user will be asked to delete.
    """

    
class AddOptions(AbstractCRUDableEntityTypeProxy):
    """
    Adds options to the interface.

    Example of descriptor, which adds two read options, "limit" and "offset", as well as an update option:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "AddOptions",
            "params": {
                "list_read_options": [
                    {
                        "name": "limit",
                        "type": "int",
                        "default": null,
                        "is_mandatory": false
                    },
                    {
                        "name": "offset",
                        "type": "int",
                        "default": null,
                        "is_mandatory": false
                    }
                ],
                "list_updator_options": [
                    {
                        "name": "add_update_date",
                        "type": "bool",
                        "default": true,
                        "is_mandatory": false
                    }
                ]
            }
        }
    """

    params: AddOptionsParams
    """
    AddOptions proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: AddOptionsParams) -> CRUDableEntityTypeInterface:
        base_interface.list_read_options=copy.deepcopy(base_interface.list_read_options)+params.list_read_options
        base_interface.list_creator_options=copy.deepcopy(base_interface.list_creator_options)+params.list_creator_options
        base_interface.list_updator_options=copy.deepcopy(base_interface.list_updator_options)+params.list_updator_options
        base_interface.list_deletor_options=copy.deepcopy(base_interface.list_deletor_options)+params.list_deletor_options
        return base_interface
    
