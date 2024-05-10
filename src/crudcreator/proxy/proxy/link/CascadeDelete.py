from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....LinkType import LinkType, Cardinality
from ....Filter import FilterInstance, FilterationEnum
from ....exceptions import EntityNotExist
from ...AbstractProxyParams import AbstractProxyParams
from ....transaction.AbstractTransaction import AbstractTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams

class CascadeDeleteParams(AbstractProxyParams):
    """
    CascadeDelete proxy settings.
    Nothing.
    """
    pass

    
class CascadeDelete(AbstractCRUDableEntityTypeProxy):
    """
    Changes the delete into a "cascade delete".
    Changes the delete behavior if the current entity is linked to another entity,
    and the destination entity must be linked to one and only one source entity (one-to-\* link).
    In this case, if the current entity is deleted,
    destination entities linked to the current deleted entity are also deleted.
    Must be preceded by at least one :ref:`create_link` to specify links.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "CascadeDelete",
            "params": {}
        }

    Which could be preceded by the following descriptor:

    .. highlight:: json
    .. code-block:: json

        {
            "name": "CreateLink",
            "params": {
                "list_linked_field": [
                    {
                        "field_name": "field_to_join",
                        "link": {
                            "entity_type_linked_to": "$entity_bis$",
                            "field_name_linked_to": "field_to_be_joined",
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

    params: CascadeDeleteParams
    """
    CascadeDelete proxy settings.
    """

    async def delete(self, params: DeleteParams):
        """
        Scans all links of the entity type, and if the link has the correct cardinality, 
        deletes the linked destination entities. 
        Then deletes the current entity.

        :raises EntityNotExist:
            If the destination entity, to which the deleted source is linked, does not exist, while the link
            stipulates that the source must be linked to at least one destination.
        """
        #TODO : it could be avoided if there were no one-to-one link*.
        list_row = await self.read(
            ReadParams(
                transaction=params.transaction,
                list_filter_instance=[
                    FilterInstance(
                        field_name=field_name,
                        filter_value=params.dict_deletor_value[field_name],
                        filtration_type=FilterationEnum.equal
                    )
                    for field_name in params.dict_deletor_value
                ],
                list_read_field=self.interface.get_readable_field_name(),
                dict_read_options={},
                limit=None,
                offset=None,
                must_read_distinct=False,
                list_field_on_which_to_sort=[],
            )
        )
        for row in list_row:
            for field in self.interface.fields.list_field:
                if field.link is not None:
                    if field.link.type.source.max == Cardinality.one and field.link.type.source.min == Cardinality.one:
                        """
                        If the destination is to be linked to one and only one source, then the
                        when the source is deleted
                        """
                        try:
                            await field.link.entity_type_linked_to.delete(
                                DeleteParams(
                                    transaction=params.transaction, 
                                    dict_deletor_value={field.link.field_name_linked_to:row[field.name]},
                                    dict_deletor_options=params.dict_deletor_options
                                )
                            )
                        except EntityNotExist as e:
                            #only tolerated if source can be linked to zero destination
                            #if not, there's a problem in the database
                            if field.link.type.dest.min != Cardinality.zero:
                                raise e#TODO : Anything other than EntityNotExist?
        return await self.base.delete(params)
    
    