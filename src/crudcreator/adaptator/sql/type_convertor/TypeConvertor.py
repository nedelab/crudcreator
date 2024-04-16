from typing import Any
from sqlalchemy.sql.sqltypes import TEXT, VARCHAR, CHAR, NCHAR, NVARCHAR, CLOB
from sqlalchemy.sql.sqltypes import INTEGER, BIGINT, DECIMAL, FLOAT, INT, NUMERIC, REAL, SMALLINT
from sqlalchemy.sql.sqltypes import BOOLEAN
from sqlalchemy.sql.sqltypes import DATE, DATETIME, TIMESTAMP
from sqlalchemy.sql.sqltypes import BINARY, BLOB, VARBINARY
from sqlalchemy.sql.sqltypes import Integer, Boolean, Date, DateTime, Time, Numeric, String, LargeBinary
from datetime import date, datetime, time
from pydantic import constr

class TypeConvertor():

    def convert(self, sql_type: Any) -> Any:
        """
        Converts an SQLAlchemy type to a Python/Pydantic type
        """
        if isinstance(sql_type, String):
            return constr(
                max_length=sql_type.length
            )
        elif isinstance(sql_type, Integer):
            return int
        elif isinstance(sql_type, Numeric):
            return float
        elif isinstance(sql_type, Boolean):
            return bool
        elif isinstance(sql_type, Date):
            return date
        elif isinstance(sql_type, DateTime):
            return datetime
        elif isinstance(sql_type, Time):
            return datetime
        elif isinstance(sql_type, LargeBinary):
            return bytes
        else:
            raise NotImplementedError()