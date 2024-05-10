
from ...source.AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ...source.AbstractSourceParams import AbstractSourceParams
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ...source.source.SQLSource import SQLSource, SQLSourceParams
from .proxy.SQLRequestConstructor import SQLRequestConstructor, SQLRequestConstructorParams
from .proxy.SQLFilter import SQLFilter, SQLFilterParams
from .proxy.SQLSort import SQLSort, SQLSortParams
from .proxy.SQLPagination import SQLPagination, SQLPaginationParams
from .proxy.SQLRequestExecutor import SQLRequestExecutor, SQLRequestExecutorParams
from .proxy.SQLCreateLink import SQLCreateLink, SQLCreateLinkParams
from .proxy.SQLReadFromLink import SQLReadFromLink, SQLReadFromLinkParams
from pydantic import BaseModel
from ..AbstractAdaptator import AbstractAdaptator, AbstractAdaptatorParams
from ...Link import LinkedFieldToSource, LinkedField, Link

class SimpleSQLAdaptatorParams(AbstractAdaptatorParams, SQLSourceParams, SQLReadFromLinkParams):

    list_linked_field: list[LinkedFieldToSource] = []
    """
    List of links.
    The order is important. It determines the order in which the join is made.
    In particular, names are given priority to columns in the first join.
    """

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
        entity = SQLRequestConstructor.build(
                    proxy_params=SQLRequestConstructorParams(),
                    base=await SQLSource.build(
                        interface=interface,
                        source_params=source_params
                    ).complete()
                )
        if len(source_params.list_linked_field) > 0:
            for linked_field in source_params.list_linked_field:
                entity = SQLReadFromLink.build(
                    proxy_params=SQLReadFromLinkParams(
                        list_activate_entity_only_on_option=source_params.list_activate_entity_only_on_option
                    ),
                    base=SQLCreateLink.build(
                        proxy_params=SQLCreateLinkParams(
                            list_linked_field=[
                                LinkedField(
                                    field_name=linked_field.field_name,
                                    link=Link(
                                        field_name_linked_to=linked_field.link.field_name_linked_to,
                                        type=linked_field.link.type,
                                        entity_type_linked_to=SQLRequestConstructor.build(
                                            proxy_params=SQLRequestConstructorParams(),
                                            base=await SQLSource.build(
                                                interface=CRUDableEntityTypeInterface(
                                                    name=linked_field.link.source_name_linked_to,
                                                    can_indicate_read_distinct=False
                                                ),
                                                source_params=source_params
                                            ).complete()
                                        )
                                    )
                                )
                            ]
                        ),
                        base=entity
                    )
                )
        return SQLRequestExecutor.build(
            proxy_params=SQLRequestExecutorParams(),
            base=SQLPagination.build(
                proxy_params=SQLPaginationParams(),
                base=SQLSort.build(
                    proxy_params=SQLSortParams(),
                    base=SQLFilter.build(
                        proxy_params=SQLFilterParams(),
                        base=entity
                    )
                )
            )
        )