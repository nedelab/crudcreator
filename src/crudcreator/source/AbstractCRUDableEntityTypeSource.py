from typing import Any
from ..AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ..Fields import Fields
from .AbstractSourceParams import AbstractSourceParams

class AbstractCRUDableEntityTypeSource(AbstractCRUDableEntityType):
    """
    A source module.
    Represents a type of entity that is plugged directly into a source.
    """

    params: AbstractSourceParams
    """
    Parameters for customizing the source module.
    It's up to the AbstractSourceParams implementations to build themselves as they should.
    """
    
    def complete(self) -> "AbstractCRUDableEntityTypeSource":
        """
        To complete the entity's interface using the information
        that can be extracted from the external source.
        """
        raise NotImplementedError()
    