
from sqlalchemy.engine import Connection, Inspector, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from pydantic import BaseModel, ConfigDict
from sqlalchemy import inspect
from typing import Any

class AbstractSQLInspectorWrapper(BaseModel):
    """
    Wraps an SQLAlchemy inspector.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def get_pk_constraint(self, table_name: str, schema_name: str):
        raise NotImplementedError()
    
    async def get_columns(self, table_name: str, schema_name: str):
        raise NotImplementedError()
    
class SQLInspectorSyncWrapper(AbstractSQLInspectorWrapper):
    """
    Wraps an SQLAlchemy inspector from a synchronous engine (but the interface remains asynchronous)
    """

    engine: Engine
    
    async def get_pk_constraint(self, table_name: str, schema_name: str) -> dict[str, Any]:
        inspector: Inspector = inspect(self.engine)
        return inspector.get_pk_constraint(table_name, schema_name)
    
    async def get_columns(self, table_name: str, schema_name: str):
        inspector: Inspector = inspect(self.engine)
        return inspector.get_columns(table_name, schema_name)
    
    
class SQLInspectorAsyncWrapper(AbstractSQLInspectorWrapper):
    """
    Wraps an SQLAlchemy inspector from an asynchronous engine
    """
    
    engine: AsyncEngine

    def _get_pk_constraint(self, conn: AsyncConnection, table_name: str, schema_name: str) -> dict[str, Any]:
        inspector: Inspector = inspect(conn)
        return inspector.get_pk_constraint(table_name, schema_name)
    
    def _get_columns(self, conn: AsyncConnection, table_name: str, schema_name: str):
        inspector: Inspector = inspect(conn)
        return inspector.get_columns(table_name, schema_name)
        
    async def get_pk_constraint(self, table_name: str, schema_name: str) -> dict[str, Any]:
        async with self.engine.connect() as conn:
            return await conn.run_sync(lambda conn: self._get_pk_constraint(conn, table_name, schema_name))
    
    async def get_columns(self, table_name: str, schema_name: str):
        async with self.engine.connect() as conn:
            return await conn.run_sync(lambda conn: self._get_columns(conn, table_name, schema_name))
    