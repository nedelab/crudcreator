
from typing import Any
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
from sqlalchemy import Select

class SQLPaginationParams(AbstractSQLRequestProxyParams):
    """
    SQLPagination proxy settings.
    Nothing.
    """

class SQLPagination(AbstractSQLRequestProxy):
    """
    Transforms the "limit" and an "offset" in the CRUD query into "limit" and an "offset" SQL clauses 
    and adds them to the SQL query.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLPagination",
            "params": {}
        }
        
    """

    params: SQLPaginationParams
    """
    SQLPagination proxy parameters.
    """
        
    async def read(self, params: ReadParams) -> Select:
        """
        Retrieves the next proxy select, then adds the limit and offset clauses (if the params are set).
        """
        req = await self.base.read(params)
        if params.limit is not None:
            req = req.limit(params.limit)
        if params.offset is not None:
            req = req.offset(params.offset)
        return req
