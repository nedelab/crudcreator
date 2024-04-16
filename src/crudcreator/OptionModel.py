from pydantic import BaseModel
from typing import Any

class OptionModel(BaseModel):
    """
    An instance of this class represents a type of option passed to a CRUD function, to modify its behavior.
    """

    name: str
    """
    Option name.
    """

    type: Any
    """
    Its Python type.
    """

    default: Any = None
    """
    Default option value if not specified.
    """

    is_mandatory: bool
    """
    Is the option mandatory in the CRUD request?
    """