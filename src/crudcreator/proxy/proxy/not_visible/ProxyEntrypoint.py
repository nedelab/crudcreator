from typing import Any
from pydantic import BaseModel, create_model, validator
from typing import Optional
from ....Sentinel import Sentinel
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ...AbstractProxyParams import AbstractProxyParams
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools

class ProxyEntrypointParams(AbstractProxyParams):
    pass
  
class ProxyEntrypoint(AbstractCRUDableEntityTypeProxy):
    """
    It hard-codes certain things to be done before starting one of the CRUD functions.
    The CRUD user has no knowledge of this proxy, and will never add it himself.
    The constructor must hard-code it as soon as it has built a CRUD entity.
    """

    params: ProxyEntrypointParams
    
    async def create(self, params: CreateParams):
        await self.check_integrity(params.transaction, params.dict_creator_value)
        return await self.base.create(params)
    
    async def update(self, params: UpdateParams):
        dict_new_values = {}
        check_integrity = False
        #integrity is checked only if one of the id fields is modified
        for k in params.dict_ids:
            if k in params.dict_updator_value and params.dict_updator_value[k] != params.dict_ids[k]:
                check_integrity = True
            dict_new_values[k] = params.dict_ids[k]
        if check_integrity:
            dict_new_values = {**dict_new_values, **params.dict_updator_value}
            await self.check_integrity(params.transaction, dict_new_values)
        
        return await self.base.update(params)
    

    