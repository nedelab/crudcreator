from typing import Any
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ...Filter import FilterInstance
from ..AbstractProxyParams import AbstractProxyParams
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from pydantic import BaseModel

class IdValue(BaseModel):
    name: str
    """
    The name of the id field.
    """

    value: Any
    """
    The value to be added. Can be a function that returns the id.
    Never read this attribute directly, but use the "get_value" function.
    TODO : check that the value type is compatible with the field type
    """

    def get_value(self):
        """
        Returns "self.value" if the attribute is not callable.
        Otherwise executes "self.value" and returns whatever the callable returns.
        """
        if callable(self.value):
            return self.value()
        else:
            return self.value

class AddIdValueParams(AbstractProxyParams):
    """
    AddIdValue proxy settings.
    """
    
    list_ids_value: list[IdValue]#TODO : separates delete and update ids ?
    """
    List of ids to be added to CRUD requests.
    """
    
    
class AddIdValue(AbstractCRUDableEntityTypeProxy):
    """
    Adds hard-coded ids to CRUD update and delete requests.
    The ids are used to select the entity to be updated or deleted.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "AddIdValue",
            "params": {
                "list_ids_value": [
                    {
                        "name": "field_1",
                        "value": 1
                    }
                ]
            }
        }
    """
    
    params: AddIdValueParams
    """
    AddIdValue proxy settings.
    """

    #TODO : may cause problems for check_integrity

    #TODO : no create ?

    async def update(self, params: UpdateParams):
        """
        Adds the ids to the CRUD request, then forwards the request to the next proxy.
        """
        return await self.base.update(
                    UpdateParams(
                        transaction=params.transaction, 
                        dict_ids=(
                            params.dict_ids |
                            {
                               id_value.name:id_value.get_value() for id_value in self.params.list_ids_value
                            }
                        ), 
                        dict_updator_value=params.dict_updator_value,
                        dict_updator_options=params.dict_updator_options
                    )
                )
    
    async def delete(self, params: DeleteParams):
        """
        Adds the ids to the CRUD request, then forwards the request to the next proxy.
        """
        return await self.base.delete(
                DeleteParams(
                    transaction=params.transaction, 
                    dict_deletor_value=(
                        params.dict_deletor_value |
                        {
                            id_value.name:id_value.get_value() for id_value in self.params.list_ids_value
                        }
                    ),
                    dict_deletor_options=params.dict_deletor_options
                )
            )