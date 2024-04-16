from enum import Enum
from pydantic import BaseModel

class Cardinality(Enum):
    """
    Represents a number of entities.
    """

    zero: str = "zero"
    """
    zero
    """

    one: str = "one"
    """
    one
    """

    many: str = "many"
    """
    many
    """

class CardinalityRange(BaseModel):
    """
    Cardinality interval.
    """

    min: Cardinality
    """
    The lower bound of the interval.
    """

    max: Cardinality
    """
    The upper bound of the interval.
    """

class LinkType(BaseModel):
    """
    Represents the cardinality of a relationship between two types of entities
    ("one-to-one", "one-to-many", 'many-to-many", "zero or one - to - many", etc).
    """

    source: CardinalityRange
    """
    The number of source entities allowed.
    """

    dest: CardinalityRange
    """
    The number of destination entities allowed.
    """
