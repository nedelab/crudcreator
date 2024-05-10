
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
from ...transaction.sql.SQLTransaction import SQLTransaction
from ..AbstractSourceParams import AbstractSourceParams
from ...adaptator.sql.engine_wrapper.SQLEngineWrapper import AbstractSQLEngineWrapper
from ...adaptator.sql.AbstractSQLEntityType import AbstractSQLEntityType
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface

class SQLSourceParams(AbstractSourceParams):
    engine_wrapper: AbstractSQLEngineWrapper
    """
    L'objet qui permet à CRUDCreator d'interagir avec la base de données SQL.
    """


class SQLSource(AbstractSQLEntityType, AbstractCRUDableEntityTypeSource):
    """
    Represents a type of entity that is plugged directly into an SQL database.
    It therefore represents an SQL table (not a database, but a table).
    
    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLSource",
            "params": {
                "engine_wrapper": "$engine_wrapper$"
            },
            "interface": {
                "name": "book",
                "fields": [
                    {
                        "name": "book_id",
                        "is_id_field": true
                    },
                    {
                        "name": "title",
                        "is_id_field": false
                    },
                    {
                        "name": "public_domain",
                        "is_id_field": false
                    }
                ]
            }
        }

    With "engine_wrapper" a substitution defined, for example, as follows:

    .. highlight:: python
    .. code-block:: python

        from sqlalchemy import create_engine
        engine = create_engine(
            f"postgresql+pg8000://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}", 
            echo=False
        )
        engine_wrapper = SQLEngineSyncWrapper(engine=engine)

    """

    params: SQLSourceParams
    """
    Source parameters.
    """

    #interface: CRUDableEntityTypeInterface#TODO : must be SQLEntityTypeInterface
    """
    The entity model associated with the table (potentially incomplete, and completed by the "complete" method).
    """

    sql_inspector: Optional[SQLColumnInspector] = None
    """
    A utility that allows us to analyze the source (among other things, to complete the interface attribute).
    Will be built by get_inspector.
    Will be used by proxies built on top of this one.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def get_inspector(self) -> SQLColumnInspector:
        """
        Returns the sql_inspector.
        Builds it if it has not already been built.
        """
        if self.sql_inspector is None:
            self.sql_inspector = await SQLColumnInspector.build_from_interface(self.params.engine_wrapper, self.interface)
        return self.sql_inspector

    async def complete(self) -> "SQLSource":
        """
        Completes the "interface" attribute with information that can be retrieved from the SQL database.
        """
        #TODO : complete link (foreign key). comment savoir si one-to-one ou many-to-many ?
        
        for field in self.interface.fields.list_field:
            column = (await self.get_inspector()).index_column[field.name]
            field_type = TypeConvertor().convert(column.type)#on convertit le type SQL en type Python
            default_value = column.default
            field.nullable = column.nullable if field.nullable is Sentinel.unknown else field.nullable
            if field.nullable:
                field_type = Optional[field_type]
            else:
                if default_value is None:
                    default_value = ...#indique qu'il n'y a pas de valeur par défaut
            field.type = field_type if field.type is Sentinel.unknown else field.type
            field.default = default_value if field.default is Sentinel.unknown else field.default
            field.is_id_field = column.primary_key if field.is_id_field is Sentinel.unknown else field.is_id_field
            field.is_automatically_generated = column.autoincrement if field.is_automatically_generated is Sentinel.unknown else field.is_automatically_generated
        return self
        