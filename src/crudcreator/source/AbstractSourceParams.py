from pydantic import BaseModel

class AbstractSourceParams(BaseModel):
    """
    Parameters for customizing the source module.
    It's up to the AbstractSourceParams implementations to build themselves as they should.
    """
    pass