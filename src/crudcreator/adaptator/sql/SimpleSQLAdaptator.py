
from ...source.AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ...source.AbstractSourceParams import AbstractSourceParams
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ...source.source.SQLSource import SQLSource, SQLSourceParams
from .proxy.SQLRequestConstructor import SQLRequestConstructor, SQLRequestConstructorParams
from .proxy.SQLFilter import SQLFilter, SQLFilterParams
from .proxy.SQLSort import SQLSort, SQLSortParams
from .proxy.SQLPagination import SQLPagination, SQLPaginationParams
from .proxy.SQLRequestExecutor import SQLRequestExecutor, SQLRequestExecutorParams
from pydantic import BaseModel
from ..AbstractAdaptator import AbstractAdaptator, AbstractAdaptatorParams

class SimpleSQLAdaptatorParams(AbstractAdaptatorParams, SQLSourceParams):
    pass

class SimpleSQLAdaptator(AbstractAdaptator):

    params: SimpleSQLAdaptatorParams#TODO : not clean, useful only for giving type to AbstractDescriptor

    @classmethod
    async def build(
        cls,
        source_params: SimpleSQLAdaptatorParams,
        interface: CRUDableEntityTypeInterface
    ) -> "AbstractCRUDableEntityTypeSource":
        """
        Method to call to instantiate the adaptator.

        :param source_params:
            See above.

        :param interface:
            See above.
        """
        return SQLRequestExecutor.build(
            proxy_params=SQLRequestExecutorParams(),
            base=SQLPagination.build(
                proxy_params=SQLPaginationParams(),
                base=SQLSort.build(
                    proxy_params=SQLSortParams(),
                    base=SQLFilter.build(
                        proxy_params=SQLFilterParams(),
                        base=SQLRequestConstructor.build(
                           proxy_params=SQLRequestConstructorParams(),
                           base=await SQLSource.build(
                                interface=interface,
                                source_params=source_params
                            ).complete()
                        )
                    )
                )
            )
        )