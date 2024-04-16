from enum import Enum
from pydantic import BaseModel
from typing import Any

class FilterationEnum(str, Enum):
    """
    Different ways of filtering on a field.
    """

    equal: str = "equal"
    """
    Field value must match filter value exactly.
    """

    contain: str = "contain"
    """
    Field value must contain filter value.
    """

    pattern: str = "pattern"
    """
    The field value must match the pattern.

    % : zero, one or more characters.

    _ : one character.
    """

    different_of: str = "different_of"
    """
    Field value must be different from filter value.
    """

    min: str = "min"
    """
    The value of the field must be at least that of the filter.
    """

    max: str = "max"
    """
    The field value must not exceed the filter value.
    """

class FilterType(BaseModel):
    """
    An instance of this class represents a filter scheme on a field.
    """

    filtration_type: FilterationEnum
    """
    How to filter the field?
    """

    is_mandatory: bool
    """
    Is the filter mandatory?
    """

    default: Any = None
    """
    What value should be given to the filter if it is not filled in?
    """

    force_long_name: bool = False

class FilterInstance(BaseModel):
    """
    Represents a filter instance on a field.
    """

    field_name: str
    """
    The name of the field to filter on.
    """

    filter_value: Any
    """
    The value to filter with.
    """

    filtration_type: FilterationEnum
    """
    How to filter the field?
    """