
from typing import Any, Type, Optional
from ....Filter import FilterationEnum
from sqlalchemy import MetaData, Table, Column, select, insert, delete, update, inspect
from sqlalchemy.engine import Inspector, Engine
from sqlalchemy.sql import Select, Delete, Insert, Update
from pydantic import BaseModel, ConfigDict
from typing import Callable
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....Sentinel import Sentinel
from ....Filter import FilterInstance
from ..SQLColumnInspector import SQLColumnInspector
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from ....proxy.AbstractProxyParams import AbstractProxyParams
from ....transaction.sql.SQLTransaction import SQLTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from sqlalchemy.ext.asyncio import AsyncEngine

class SQLRequestConstructorParams(AbstractSQLRequestProxyParams):
    """
    SQLRequestConstructor proxy parameters.
    """

    read_distinct: bool
    """
    Should select indicate "distinct"?
    """
    
class SQLRequestConstructor(AbstractSQLRequestProxy):
    """
    The first of the SQL proxies.
    This is the module that will create the query skeleton, from which subsequent modules will work.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLRequestConstructor",
            "params": {
                "read_distinct": false
            }
        }
    """

    params: SQLRequestConstructorParams
    """
    SQLRequestConstructor proxy parameters.
    """

    #TODO : base constraint: must not define read, update, etc.

    model_config = ConfigDict(arbitrary_types_allowed=True)

    #TODO : a proxy to whitelist list_read_field
    async def read(self, params: ReadParams) -> Select:
        """
        Builds a simple "select" (or "select distinct"),
        whose list of SQL columns corresponds to the list of "list_read_field" fields
        given as parameters to the CRUD request.
        """
        req: Select = select(*[
            (await self.get_inspector()).index_sqlalchemy_column[field_name].label(field_name)
            for field_name in params.list_read_field
            if field_name in (await self.get_inspector()).index_sqlalchemy_column
            and field_name in self.interface.fields.index_field_by_name
        ])  
        if self.params.read_distinct:
            req = req.distinct()
        return req
    
    async def create(self, params: CreateParams) -> Insert:
        """
        Builds a simple insert,
        whose list of SQL columns corresponds to the list of "dict_creator_value" fields
        given as parameters to the CRUD request.
        """
        return insert((await self.get_inspector()).table).values(**params.dict_creator_value)

    async def delete(self, params: DeleteParams) -> Delete:
        """
        Builds a simple "delete", with a where clause on the ids given as parameters to the CRUD request.
        """
        req = delete((await self.get_inspector()).table)
        for field_name in params.dict_deletor_value:
            if params.dict_deletor_value[field_name] is not None:
                column = (await self.get_inspector()).table.columns.get(field_name)
                req = req.where(column == params.dict_deletor_value[field_name])
        return req

    async def update(self, params: UpdateParams) -> Optional[Update]:
        """
        Builds a simple "update",
        whose list of SQL columns corresponds to the list of "dict_updator_value" fields
        given as parameters to the CRUD request.
        Adds the where clause to the ids given as CRUD query parameters.
        If all dict_updator_value values are set to None, i.e. if no column is to be
        to be updated, no query is returned (None is returned).
        """
        dict_value = {}
        for field_name in params.dict_updator_value:
            if params.dict_updator_value[field_name] is not None:
                dict_value[field_name] = params.dict_updator_value[field_name]
        if len(dict_value.keys()) == 0:#TODO : meilleur gestion d'erreur
            return None
        req = update((await self.get_inspector()).table).values(**dict_value)
        for field_name in params.dict_ids:
            if params.dict_ids[field_name] is not None:
                column = (await self.get_inspector()).table.columns.get(field_name)
                req = req.where(column == params.dict_ids[field_name])
        return req
