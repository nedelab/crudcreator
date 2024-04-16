from pydantic import BaseModel

class AbstractTransaction(BaseModel):
    """
    Represents a CRUD transaction in progress.
    """
    pass