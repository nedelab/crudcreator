
from pydantic import BaseModel
from typing import Optional, Any

class SQLColumn(BaseModel):
    """
    An instance of this class represents a column information extracted from a SQL database.
    """

    name: Optional[str] = None
    """
    The column name.
    """

    type: Optional[Any] = None
    """
    Its SQLAlchemy type.
    """

    nullable: Optional[bool] = None
    """
    Can the column have null values?
    """

    default: Optional[Any] = None
    """
    The default value for the column.
    """

    primary_key: Optional[bool] = None
    """
    Is it a primary key.
    """

    autoincrement: Optional[bool] = None
    """
    Is it autoincremented when the row is created?
    """