
from typing import Any, Type, Optional
from sqlalchemy import MetaData, Table, Column, select, insert, delete, update, inspect
from sqlalchemy.engine import Inspector, Engine
from sqlalchemy.sql import Select, Delete, Insert, Update
from pydantic import BaseModel
from typing import Callable
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....Sentinel import Sentinel
from ....Filter import FilterInstance
from ....proxy.AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ..SQLColumnInspector import SQLColumnInspector
from ....proxy.AbstractProxyParams import AbstractProxyParams
from ..SQLEntityTypeInterface import SQLEntityTypeInterface
from ....transaction.sql.SQLTransaction import SQLTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from ..AbstractSQLEntityType import AbstractSQLEntityType
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface

class AbstractSQLRequestProxyParams(AbstractProxyParams):
    pass
    
class AbstractSQLRequestProxy(AbstractSQLEntityType, AbstractCRUDableEntityTypeProxy):
    """
    A type of proxy that manipulates SQL queries.
    These CRUD actions don't return data, but SQLAlchemy queries.
    """

    params: AbstractSQLRequestProxyParams
    interface: CRUDableEntityTypeInterface#TODO : must be SQLEntityTypeInterface
    base: AbstractSQLEntityType

    async def get_inspector(self) -> SQLColumnInspector:
        """
        Returns the inspector that will allow the various proxies to interact with SQLAlchemy tables and columns.
        """
        return await self.base.get_inspector()

    async def read(self, params: ReadParams) -> Select:
        """
        Must return a "select" SQLAlchemy request.
        """
        return await self.base.read(params)
    
    async def create(self, params: CreateParams) -> Insert:
        """
        Must return an "insert" SQLAlchemy request.
        """
        return await self.base.create(params)

    async def delete(self, params: DeleteParams) -> Delete:
        """
        Must return a "delete" SQLAlchemy request.
        """
        return await self.base.delete(params)

    async def update(self, params: UpdateParams) -> Optional[Update]:
        """
        Must return an "update" SQLAlchemy request (if an update is required).
        Otherwise returns None.
        """
        return await self.base.update(params)