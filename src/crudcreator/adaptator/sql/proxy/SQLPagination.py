
from typing import Any
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams

class SQLPaginationParams(AbstractSQLRequestProxyParams):
    """
    SQLPagination proxy settings.
    """

    limit_option_name: str
    """
    The option that specifies the "limit" value to be added to the SQL query.
    """

    offset_option_name: str
    """
    The option that sets the offset value to be added to the SQL query.
    """

class SQLPagination(AbstractSQLRequestProxy):
    """
    Adds a "limit" and an "offset" to the SQL query, on option.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLPagination",
            "params": {
                "limit_option_name": "my_limit",
                "offset_option_name": "my_offset"
            }
        }
        
    """

    params: SQLPaginationParams
    """
    SQLPagination proxy parameters.
    """
        
    async def read(self, params: ReadParams) -> list[Any]:
        """
        Retrieves the next proxy select, then adds the limit and offset clauses (if the options are set).
        """
        req = await self.base.read(params)
        if self.params.limit_option_name in params.dict_read_options and params.dict_read_options[self.params.limit_option_name] is not None:
            req = req.limit(params.dict_read_options[self.params.limit_option_name])
        if self.params.offset_option_name in params.dict_read_options and params.dict_read_options[self.params.offset_option_name] is not None:
            req = req.offset(params.dict_read_options[self.params.offset_option_name])
        return req
