from pydantic import BaseModel, ConfigDict
import functools

class AbstractProxyParams(BaseModel):
    """
    Parameters for customizing a proxy.
    It's up to the AbstractProxyParams implementations to build as they should.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True, ignored_types=(functools.cached_property, ))