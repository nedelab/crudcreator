from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ....Sentinel import Sentinel
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Fields import Fields
from ....Filter import FilterInstance, FilterationEnum
from enum import Enum
from ....Link import Link
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from sqlalchemy.sql import Select, Delete, Insert, Update
from sqlalchemy import Column
from ..SQLColumnInspector import SQLColumnInspector
from ....transaction.sql.SQLTransaction import SQLTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams

class SQLFilterParams(AbstractSQLRequestProxyParams):
    """
    SQLFilter proxy parameters.
    No parameters.
    """
    pass
    
class SQLFilter(AbstractSQLRequestProxy):
    """
    Transforms the filter instances in the CRUD query into "where clauses" and adds them to the SQL query.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLFilter",
            "params": {}
        }
    """

    params: SQLFilterParams
    """
    SQLFilter proxy settings.
    """

    async def read(self, params: ReadParams) -> Select:
        """
        Retrieves the next proxy select, then adds all where clauses that correspond
        to the filter instances given in the CRUD request.
        """
        req = await self.base.read(params)
        index_field = self.interface.fields.index_field_by_name
        for filter_instance in params.list_filter_instance:
            field = index_field[filter_instance.field_name]
            if field.list_allowed_filter_type is not None and filter_instance.filtration_type not in field.list_allowed_filter_type:
                raise Exception()#TODO : meilleur gestion erreur
            column = (await self.get_inspector()).index_sqlalchemy_column[field.name]
            if filter_instance.filtration_type == FilterationEnum.equal:
                req = req.where(column == filter_instance.filter_value)
            elif filter_instance.filtration_type == FilterationEnum.contain:#TODO : case sensitive ?
                req = req.where(column.ilike("%"+filter_instance.filter_value+"%"))
            elif filter_instance.filtration_type == FilterationEnum.pattern:#TODO : case sensitive ?
                req = req.where(column.ilike(filter_instance.filter_value))
            elif filter_instance.filtration_type == FilterationEnum.different_of:
                req = req.where(column != filter_instance.filter_value)
            elif filter_instance.filtration_type == FilterationEnum.max:
                req = req.where(column <= filter_instance.filter_value)
            elif filter_instance.filtration_type == FilterationEnum.min:
                req = req.where(column >= filter_instance.filter_value)
            else:
                raise NotImplementedError()
        return req

    
    