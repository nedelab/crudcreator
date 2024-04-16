from pydantic import BaseModel, ConfigDict
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncConnection
from ..AbstractTransaction import AbstractTransaction
from ...adaptator.sql.engine_wrapper.SQLConnectionWrapper import AbstractSQLConnectionWrapper

class SQLTransaction(AbstractTransaction):
    """
    Represents a CRUD transaction in progress, whose source is an SQL database.
    """

    sqlalchemy_connection_wrapper: AbstractSQLConnectionWrapper
    """
    The object used to interact with the SQL connection associated with the transaction.
    Is used by the SQLRequestExecutor module to execute the SQL query resulting from the CRUD request.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)