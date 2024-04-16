
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncConnection
from pydantic import BaseModel, ConfigDict

class AbstractSQLConnectionWrapper(BaseModel):
    """
    Wraps an SQLAlchemy connection.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def execute(self, req):
        """
        Executes an SQLAlchemy query.
        """
        raise NotImplementedError()
    
class SQLConnectionSyncWrapper(AbstractSQLConnectionWrapper):
    """
    Wraps a synchronous SQLAlchemy connection (but the interface remains asynchronous)
    """

    connection: Connection

    async def execute(self, req):
        """
        Executes an SQLAlchemy query.
        """
        return self.connection.execute(req)
    
class SQLConnectionAsyncWrapper(AbstractSQLConnectionWrapper):
    """
    Wraps a aynchronous SQLAlchemy connection.
    """

    connection: AsyncConnection
    
    async def execute(self, req):
        """
        Executes an SQLAlchemy query.
        """
        return await self.connection.execute(req)