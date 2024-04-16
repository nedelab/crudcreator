from src.crudcreator.OptionModel import OptionModel
from src.crudcreator.proxy.proxy.AddOptions import AddOptions, AddOptionsParams
from src.crudcreator.proxy.AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from src.crudcreator.proxy.AbstractProxyParams import AbstractProxyParams
from src.crudcreator.schema import ReadParams, CreateParams, UpdateParams, DeleteParams

class TestOptionParam(AbstractProxyParams):
    pass
class TestOption(AbstractCRUDableEntityTypeProxy):
    params: TestOptionParam

    async def read(self, params: ReadParams):
        res = await self.base.read(params)
        print(res)
        print(params.dict_read_options)
        if params.dict_read_options["add_fixed"]:
            res.append({"field_1": "read_fixed_1", "field_2": "read_fixed_2"})
        return res
    
    async def create(self, params: CreateParams):
        if params.dict_creator_options["copy_1_to_2"]:
            params.dict_creator_value["field_2"] = params.dict_creator_value["field_1"]
        return await self.base.create(params)

    async def delete(self, params: DeleteParams):
        if params.dict_deletor_options["delete_fixed"]:
            params.dict_deletor_value["field_1"] = "delete_fixed_1"
        return await self.base.delete(params)

    async def update(self, params: UpdateParams):
        if params.dict_updator_options["copy_1_to_2"]:
            params.dict_updator_value["field_2"] = params.dict_updator_value["field_1"]
        return await self.base.update(params)