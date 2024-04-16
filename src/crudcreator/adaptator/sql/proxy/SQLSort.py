
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

class SortType(Enum):
    """
    How to order?
    """

    asc: str = "asc"
    """
    Order in ascending order.
    """

    desc: str = "desc"
    """
    Order in descending order.
    """

class FieldToSort(BaseModel):
    """
    An "order by" to add to an SQL query.
    """

    field_name: str
    """
    The name of the field on which to order.
    """

    type: SortType
    """
    How to order?
    """

class SQLSortParams(AbstractSQLRequestProxyParams):
    """
    SQLSort proxy parameters.
    """
    
    list_field_to_sort: list[FieldToSort]
    """
    The "order by" list to add to the SQL query
    """

class SQLSort(AbstractSQLRequestProxy):
    """
    Adds "order by" clauses to the SQL query.

    Example of a descriptor, which will add "order by field_foo asc" and
    and "order by field_bar desc" to the SQL query:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLSort",
            "params": {
                "list_field_to_sort": [
                    {
                        "field_name": "field_foo",
                        "type": "asc"
                    },
                    {
                        "field_name": "field_bar",
                        "type": "desc"
                    }
                ]
            }
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
        for field_to_sort in self.params.list_field_to_sort:
            column_to_sort = (await self.get_inspector()).index_sqlalchemy_column[field_to_sort.field_name]
            if field_to_sort.type == SortType.asc:
                column_to_sort = column_to_sort.asc()
            elif field_to_sort.type == SortType.desc:
                column_to_sort = column_to_sort.desc()
            else:
                raise NotADirectoryError()
            req = req.order_by(column_to_sort)
        return req
    
        
