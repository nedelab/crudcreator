from typing import Any
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ...Filter import FilterInstance
from ..AbstractProxyParams import AbstractProxyParams
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from pydantic import BaseModel

class WriteValue(BaseModel):
    name: str
    """
    The name of the id field.
    """

    value: Any
    """
    The value to be added. Can be a function that returns the value.
    Never read this attribute directly, but use the "get_value" function.
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

class AddWriteValueParams(AbstractProxyParams):
    """
    AddWriteValue proxy parameters.
    """

    list_create_value: list[WriteValue]
    """
    The list of values to be added to the creation.
    """

    list_update_value: list[WriteValue]
    """
    The list of values at update.
    """
    
    
class AddWriteValue(AbstractCRUDableEntityTypeProxy):
    """
    Adds hard-coded values to creation or update.

    Example of descriptor, which adds a new value at creation (creation date),
    and a new value at update (the update date):

    .. highlight:: json
    .. code-block:: json

        {
            "name": "AddWriteValue",
            "params": {
                "list_create_value": [
                    {
                        "name": "creation_date",
                        "value": "$now$"
                    }
                ],
                
                "list_update_value": [
                    {
                        "name": "last_update_date",
                        "value": "$now$"
                    }
                ]
            }
        }

    With "now" a substitution defined as follows:

    .. highlight:: python
    .. code-block:: python

        "now": datetime.now

    """
    
    params: AddWriteValueParams
    """
    AddWriteValue proxy parameters.
    """

    #TODO : peut poser problème pour le check_integrity (doit savoir si la valeur générée est unique ou non ?)
    #car on ne peut pas générer la valeur pour le check_integrity, elle reste d'être différente de celle générée au moment du create

    async def update(self, params: UpdateParams):
        """
        Adds the new values to the CRUD request, then forwards the request to the next proxy.
        """
        return await self.base.update(
                    UpdateParams(
                        transaction=params.transaction, 
                        dict_ids=params.dict_ids, 
                        dict_updator_value=(
                            params.dict_updator_value |
                            {
                               write_value.name:write_value.get_value() for write_value in self.params.list_update_value
                            }
                        ),
                        dict_updator_options=params.dict_updator_options
                    )
                )
    
    async def create(self, params: CreateParams):
        """
        Adds the new values to the CRUD request, then forwards the request to the next proxy.
        """
        return await self.base.create(
                CreateParams(
                    transaction=params.transaction, 
                    dict_creator_value=(
                        params.dict_creator_value | 
                        {
                            write_value.name:write_value.get_value() for write_value in self.params.list_create_value
                        }
                    ),
                    dict_creator_options=params.dict_creator_options
                )
            )