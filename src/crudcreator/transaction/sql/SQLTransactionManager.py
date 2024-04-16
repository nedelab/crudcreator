from contextlib import asynccontextmanager
from .SQLTransaction import SQLTransaction
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from ..AbstractTransactionManager import AbstractTransactionManager
from .SQLTransaction import SQLTransaction
from ...adaptator.sql.engine_wrapper.SQLEngineWrapper import AbstractSQLEngineWrapper
from pydantic import ConfigDict

class SQLTransactionManager(AbstractTransactionManager):
    """
    Used to initiate and terminate CRUD transactions whose source is an SQL database.
    """

    engine_wrapper: AbstractSQLEngineWrapper
    """
    The object through which to interact with the SQL database.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @asynccontextmanager
    async def begin(self) -> SQLTransaction:
        """
        Context manager that yields a new CRUD transaction whose source is an SQL database.
        """
        async with self.engine_wrapper.begin() as sqlalchemy_connection_wrapper:
            yield SQLTransaction(sqlalchemy_connection_wrapper=sqlalchemy_connection_wrapper)