
from contextlib import asynccontextmanager
from typing import Iterator
from sqlalchemy.engine import Engine, Inspector
from sqlalchemy.ext.asyncio import AsyncEngine
from .SQLConnectionWrapper import AbstractSQLConnectionWrapper, SQLConnectionSyncWrapper, SQLConnectionAsyncWrapper
from pydantic import BaseModel, ConfigDict
from sqlalchemy import inspect
import asyncio
from .SQLInspectorWrapper import SQLInspectorSyncWrapper, SQLInspectorAsyncWrapper, AbstractSQLInspectorWrapper

class AbstractSQLEngineWrapper(BaseModel):
    """
    Wraps an SQLAlchemy engine.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @asynccontextmanager
    async def begin(self) -> Iterator[AbstractSQLConnectionWrapper]:
        """
        To be implemented in a child class.
        Creates a connection and initiates a transaction with the database.
        """
        raise NotImplementedError()
    
    async def execute(self, req):
        """
        Executes an SQLAlchemy query.
        """
        async with self.begin() as connection:
            return await connection.execute(req)
    
    def inspect(self) -> AbstractSQLInspectorWrapper:
        """
        Returns the object wrapping an SQLAlchemy Inspector.
        """
        raise NotImplementedError()
    

class SQLEngineSyncWrapper(AbstractSQLEngineWrapper):
    """
    Wraps a synchronous SQLAlchemy engine (but the interface remains asynchronous).
    """

    engine: Engine

    @asynccontextmanager
    async def begin(self) -> Iterator[SQLConnectionSyncWrapper]:
        """
        Creates a connection and initiates a transaction with the database.
        """
        with self.engine.begin() as connection:
            yield SQLConnectionSyncWrapper(connection=connection)

    def inspect(self) -> SQLInspectorSyncWrapper:
        """
        Returns the object wrapping an SQLAlchemy Inspector.
        """
        return SQLInspectorSyncWrapper(engine=self.engine)
    

class SQLEngineAsyncWrapper(AbstractSQLEngineWrapper):
    """
    Wraps a asynchronous SQLAlchemy engine.
    """

    engine: AsyncEngine

    @asynccontextmanager
    async def begin(self) -> Iterator[SQLConnectionAsyncWrapper]:
        """
        Creates a connection and initiates a transaction with the database.
        """
        async with self.engine.begin() as connection:
            yield SQLConnectionAsyncWrapper(connection=connection)
    
    def inspect(self) -> SQLInspectorAsyncWrapper:
        """
        Returns the object wrapping an SQLAlchemy Inspector.
        """
        return SQLInspectorAsyncWrapper(engine=self.engine)
    