from contextlib import asynccontextmanager
from .AbstractTransaction import AbstractTransaction
from pydantic import BaseModel

class AbstractTransactionManager(BaseModel):
    """
    Initiates and terminates CRUD transactions.
    """

    @asynccontextmanager
    async def begin(self) -> "AbstractTransaction":
        """
        Context manager that yields a new CRUD transaction.
        """
        raise NotImplementedError()