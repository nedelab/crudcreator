
from typing import Any, Type, Optional
from ...Filter import FilterType
from sqlalchemy import MetaData, Table, Column, select, insert, delete, update, inspect
from sqlalchemy.engine import Inspector, Engine
from sqlalchemy.sql import Select, Delete, Insert, Update
from pydantic import BaseModel, ConfigDict
from typing import Callable
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from ..AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ...Sentinel import Sentinel
from ...Filter import FilterInstance
from ...adaptator.sql.SQLColumnInspector import SQLColumnInspector
from ...adaptator.sql.type_convertor.TypeConvertor import TypeConvertor
from ...adaptator.rest.RESTEntityTypeInterface import RESTEntityTypeInterface
from ..AbstractSourceParams import AbstractSourceParams
from ...adaptator.sql.engine_wrapper.SQLEngineWrapper import AbstractSQLEngineWrapper
from ...adaptator.sql.AbstractSQLEntityType import AbstractSQLEntityType

class RESTSourceParams(AbstractSourceParams):
    base_url_read: str
    base_url_create: str
    base_url_update: str
    base_url_delete: str
    #TODO : update or create ?


class RESTSource(AbstractSQLEntityType):

    """
    TODO
    """

    params: RESTSourceParams
    interface: RESTEntityTypeInterface

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def complete(self) -> "RESTSource":
        pass
