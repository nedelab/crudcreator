
from typing import Any, Type, Optional
from ....exceptions import EntityAlreadyExist, EntityNotExist
from sqlalchemy import MetaData, Table, Column, select, insert, delete, update
from sqlalchemy.engine import Connection, Transaction
from sqlalchemy.sql import Select, Executable
from pydantic import BaseModel
from typing import Callable
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from ....proxy.AbstractProxyParams import AbstractProxyParams
from ....Sentinel import Sentinel
from .SQLRequestConstructor import SQLRequestConstructor
from ....Filter import FilterInstance
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from enum import Enum
from ..SQLColumnInspector import SQLColumnInspector
from ....transaction.sql.SQLTransaction import SQLTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from ....Sort import SortType

class SQLSortParams(AbstractSQLRequestProxyParams):
    """
    SQLSort proxy parameters.
    Nothing.
    """

class SQLSort(AbstractSQLRequestProxy):
    """
    Transforms the "sort" instances in the CRUD query into “order by” clauses and adds them to the SQL query.

    Example of a descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLSort",
            "params": {}
        }
    """
    
    params: SQLSortParams
    """
    SQLSort proxy parameters.
    """
        
    async def read(self, params: ReadParams) -> list[Any]:
        """
        Retrieves the SQL query from the following proxy. Then adds the "order by" clauses before returning the result.
        """
        req = await self.base.read(params)
        for field_to_sort in params.list_field_on_which_to_sort:
            column_to_sort = (await self.get_inspector()).index_sqlalchemy_column[field_to_sort.field_name]
            if field_to_sort.type == SortType.asc:
                column_to_sort = column_to_sort.asc()
            elif field_to_sort.type == SortType.desc:
                column_to_sort = column_to_sort.desc()
            else:
                raise NotADirectoryError()
            req = req.order_by(column_to_sort)
        return req
    
        
