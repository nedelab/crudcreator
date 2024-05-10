
from ....proxy.proxy.link.CreateLink import CreateLink, CreateLinkParams
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from ..SQLColumnInspector import SQLColumnInspector
from typing import Optional

class SQLCreateLinkParams(AbstractSQLRequestProxyParams, CreateLinkParams):
    """
    SQLCreateLink proxy parameters.
    """
    pass

class SQLCreateLink(CreateLink, AbstractSQLRequestProxy):
    """
    Adds a link to the interface.
    Does not actually transform it into a "join" in the SQL query.
    You'll have to use the :ref:`sql_read_from_link` module for that.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLCreateLink",
            "params": {
                "list_linked_field": [
                    {
                        "field_name": "column_to_join",
                        "link": {
                            "entity_type_linked_to": "$entity3_sql$",
                            "field_name_linked_to": "column_to_be_joined",
                            "type": {
                                "source": {
                                    "min": "one",
                                    "max": "one"
                                },
                                "dest": {
                                    "min": "one",
                                    "max": "one"
                                }
                            }
                        }
                    }
                ]
            }
        }
    """

    params: SQLCreateLinkParams
    """
    SQLCreateLink proxy parameters.
    """

    sql_inspector: Optional[SQLColumnInspector] = None
    """
    The new sql_inspection, which takes into account the new links between SQLAlchemy tables.
    Is built by the "get_inspector" overloaded by this class.
    """
    
    async def get_inspector(self) -> SQLColumnInspector:
        """
        Creates a new sql_inspector containing the merged SQLALchemy tables and columns.
        """
        if self.sql_inspector is None:
            inspector = (await self.base.get_inspector())
            for field in self.interface.fields.list_field:
                if field.link is not None:
                    inspector = inspector.join_inspector(await field.link.entity_type_linked_to.get_inspector())
            self.sql_inspector = inspector
        return self.sql_inspector
    
    