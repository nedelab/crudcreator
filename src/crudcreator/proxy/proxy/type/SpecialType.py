from pydantic import BaseModel, Field, field_validator
from typing import Any, Callable

class SpecialType(BaseModel):
    destination_type: Any
    """
    Destination-side field type.
    """

    source_type: Any = None
    """
    Source-side field type.
    """

    source_to_destination: Any = Field(title="Source to interface function")#Any otherwise schema_json removes it (TODO)
    """
    The function that reprocesses fields on the source side to set them to the correct type on the destination side.
    """

    destination_to_source: Any = Field(title="Interface to source function")#Any otherwise schema_json removes it (TODO)
    """
    The function that reprocesses the destination-side field to set it to the correct source-side type.
    """

    @field_validator("source_to_destination", "destination_to_source")
    def callable_type(cls, v):
        if not callable(v):
            raise ValueError(f"Not a function")
        return v

