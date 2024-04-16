
from typing import Any, Type, Optional
from ....exceptions import EntityAlreadyExist, EntityNotExist
from sqlalchemy import MetaData, Table, Column, select, insert, delete, update
from sqlalchemy.engine import Connection, Transaction
from sqlalchemy.sql import Select, Executable
from pydantic import BaseModel, ConfigDict
from typing import Callable
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from ....proxy.AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....Sentinel import Sentinel
from .SQLRequestConstructor import SQLRequestConstructor
from ....Filter import FilterInstance, FilterationEnum
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from ..SQLColumnInspector import SQLColumnInspector
from ....proxy.AbstractProxyParams import AbstractProxyParams
from ....transaction.sql.SQLTransaction import SQLTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from sqlalchemy.ext.asyncio import AsyncEngine

class SQLRequestExecutorParams(AbstractSQLRequestProxyParams):
    """
    "SQLRequestExecutor" module parameters.
    No parameters.
    """
    pass
    

class SQLRequestExecutor(
    AbstractSQLRequestProxy#TODO : l'est vraiment encore ?
):
    """
    Is the last of the SQL proxies. Is the proxy that will execute the query and return the result.
    The following proxies are generic proxies.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLRequestExecutor",
            "params": {}
        }

    """

    params: SQLRequestExecutorParams
    """
    "SQLRequestExecutor" module parameters.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def _execute_request(self, transaction: SQLTransaction, req: Executable):
        return await transaction.sqlalchemy_connection_wrapper.execute(req)
        
    async def read(self, params: ReadParams) -> list[Any]:
        """
        Retrieves the SQL query from the next proxy, then executes it.
        Transforms the result into a dictionary list, then returns it.
        """
        req = await self.base.read(params)
        ret = await self._execute_request(params.transaction, req)
        return [
            row._mapping
            for row in ret.all()
        ]

    async def create(self, params: CreateParams):
        """
        Retrieves the SQL query from the next proxy, then executes it.
        
        :raises EntityAlreadyExist:
            If SQLAlchemy raises an IntegrityError exception.

        TODO: return the ids of the created entity.
        """
        req = await self.base.create(params)
        #req = req.returning(self.get_inspector().table)
        try:
            ret = await self._execute_request(params.transaction, req)
        except IntegrityError as e:
            print(e)
            raise EntityAlreadyExist()
        #print(ret.inserted_primary_key )
        #return ret.inserted_primary_key 
        return ret

    async def delete(self, params: DeleteParams):
        """
        Retrieves the SQL query from the next proxy, then executes it.
        
        :raises EntityNotExist:
            If no entities have been deleted.
        """
        req = await self.base.delete(params)
        ret = await self._execute_request(params.transaction, req)
        if ret.rowcount == 0:#TODO : pouvoir l'autoriser (attention, si pas autorisé, il faut faire un rollback)
            raise EntityNotExist()
        #TODO : vérifier qu'un seul a été supprimé

    async def update(self, params: UpdateParams):
        """
        Retrieves the SQL query from the next proxy.
        If the query is set to None, there are no fields to update, so stop the CRUD here.
        Otherwise, execute the query.
        
        :raises EntityNotExist:
            If no entity has been updated.
        :raises EntityAlreadyExist:
            If SQLAlchemy raises an IntegrityError exception.
        """
        req = await self.base.update(params)
        if req is not None:#possible s'il n'y a rien à updater
            try:
                ret = await self._execute_request(params.transaction, req)
            except IntegrityError as e:
                print(e)
                raise EntityAlreadyExist()
            else:
                if ret.rowcount == 0:
                    raise EntityNotExist()