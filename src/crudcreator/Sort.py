from enum import Enum
from pydantic import BaseModel

class SortType(Enum):
    """
    How to order?
    """

    asc: str = "asc"
    """
    Order in ascending order.
    """

    desc: str = "desc"
    """
    Order in descending order.
    """

class FieldToSort(BaseModel):
    """
    An "order by" to add to CRUD query.
    """

    field_name: str
    """
    The name of the field on which to order.
    """

    type: SortType
    """
    How to order?
    """