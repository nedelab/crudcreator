
from sqlalchemy import MetaData, Table, Column, select, insert, delete, update, inspect, text
from sqlalchemy.engine import Inspector, Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import ProgrammingError, NoResultFound
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from .engine_wrapper.SQLEngineWrapper import AbstractSQLEngineWrapper
from .SQLEntityTypeInterface import SQLEntityTypeInterface
from .SQLColumn import SQLColumn


class SQLColumnInspector(BaseModel):
    """
    A utility for analyzing an SQL table.
    """

    list_column: list[SQLColumn]
    """
    Set by the build function.
    List of table columns and corresponding information.
    """

    index_column: dict[str, SQLColumn]
    """
    Set by the build.
    An index that associates the name of a column with its information.
    """

    list_sqlalchemy_column: list[Column]
    """
    Set by the build function.
    The list of SQLAlchemy columns (used to build queries, for example).
    """

    index_sqlalchemy_column: dict[str, Column]
    """
    Set by the build function.
    An index that associates the name of a column with the corresponding SQLAlchemy column.
    """

    table: Table
    """
    Set by the build function.
    The SQLAlchemy table.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
        
    def join_inspector(self, other_inspector: "SQLColumnInspector") -> "SQLColumnInspector":
        """
        Creates the inspector associated with a virtual table created by joining two other tables.
        """
        rename_column = {}
        for k in other_inspector.index_column:
            if k not in self.index_column:
                rename_column[k] = k
            else:
                rename_column[k] = f"{other_inspector.table.name}.{k}"
        return SQLColumnInspector(
            list_column=self.list_column+other_inspector.list_column,
            list_sqlalchemy_column=self.list_sqlalchemy_column+other_inspector.list_sqlalchemy_column,
            index_column={**self.index_column, **{rename_column[k]:v for k, v in other_inspector.index_column.items()}},
            index_sqlalchemy_column={**self.index_sqlalchemy_column, **{rename_column[k]:v for k, v in other_inspector.index_sqlalchemy_column.items()}},
            table=self.table#TODO ? Ne devrait plus être utilisé après un join
        )


    @staticmethod
    async def build_from_interface(
        sqlalchemy_engine_wrapper: AbstractSQLEngineWrapper,
        source_interface: SQLEntityTypeInterface
    ):
        """
        Builds the inspector.
        """

        #on sépare le nom de la table du schéma (TODO : faire plus propre ?)
        source_name_split = source_interface.name.split(".", 2)
        table_name = source_name_split[-1]
        schema_name = None
        if len(source_name_split) > 1:
            schema_name = source_name_split[0]

        #on lance l'inspection de la table
        inspector_wrapper = sqlalchemy_engine_wrapper.inspect()
        list_column_name_primary_key = await inspector_wrapper.get_pk_constraint(table_name, schema_name)
        list_column = []
        for c in await inspector_wrapper.get_columns(table_name, schema_name):
            if c["default"] is None:
                evaluated_default = None
            else:
                try:
                    evaluated_default = (await sqlalchemy_engine_wrapper.execute(text(f"SELECT {c['default']}"))).scalar_one()#TODO trouver plus propre (le default est une expression sql)
                    #except (ProgrammingError, NoResultFound) as e:
                except Exception as e:#TODO : faire plus propre
                    print(e)
                    evaluated_default = None
            list_column.append(
                SQLColumn(
                    name=c["name"],
                    type=c["type"],
                    nullable=c["nullable"],
                    default=evaluated_default,
                    primary_key=(c["name"] in list_column_name_primary_key["constrained_columns"]),
                    autoincrement=False if "autoincrement" not in c else (True if c["autoincrement"]=="auto" else c["autoincrement"])
                )
            )
        index_column = {
            sqlalchemy_column.name:sqlalchemy_column
            for sqlalchemy_column in list_column
        }

        #on crée les colonnes SQLAlchemy
        list_sqlalchemy_column = [
            Column(
                column.name,
                column.type,
                primary_key=column.primary_key,
                nullable=column.nullable,
                default=None,#toujours à False pour sqlalchemy, sinon c'est lui qui s'occupe 
                #d'intégrer le default dans la requête, ce qui pose problème avec les SERIAL 
                #pour lesquels sqlalchemy considère bizarrement qu'il y a un défaut 
                #(qui est l'incrément suivant pour lui)
                autoincrement=False,#toujours à False pour sqlalchemy, sinon c'est lui qui s'occupe 
                #d'autoincrémenter, et ce n'est pas ce que l'on veut
            )
            for column in list_column
        ]
        index_sqlalchemy_column = {
            sqlalchemy_column.name:sqlalchemy_column
            for sqlalchemy_column in list_sqlalchemy_column
        }

        #on crée la table SQLAlchemy
        table = Table(
                table_name, 
                MetaData(schema=schema_name), *list_sqlalchemy_column
            )
        return SQLColumnInspector(
            list_sqlalchemy_column=list_sqlalchemy_column,
            index_sqlalchemy_column=index_sqlalchemy_column,
            list_column=list_column,
            index_column=index_column,
            table=table
        )
