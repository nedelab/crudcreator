from ...AbstractCRUDableEntityType import AbstractCRUDableEntityType
from .SQLColumnInspector import SQLColumnInspector

class AbstractSQLEntityType(AbstractCRUDableEntityType):
    """
    A type of entity that handles SQL queries.
    """
    
    async def get_inspector(self) -> SQLColumnInspector:
        raise NotImplementedError()