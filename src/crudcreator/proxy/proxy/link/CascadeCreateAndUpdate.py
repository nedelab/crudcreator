from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ...AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....LinkType import LinkType, Cardinality
from ....Filter import FilterInstance, FilterationEnum
from ....exceptions import EntityNotExist
from ...AbstractProxyParams import AbstractProxyParams
from ....transaction.AbstractTransaction import AbstractTransaction
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....Fields import Fields
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams

class CascadeCreateAndUpdateParams(AbstractProxyParams):
    """
    CascadeCreateAndUpdate proxy settings.
    Nothing.
    """
    pass


class CascadeCreateAndUpdate(AbstractCRUDableEntityTypeProxy):
    """
    Changes the create and update into a "cascade create" or "cascade update".
    Changes the create and update behavior if the current entity is linked to another entity,
    and the source entity must be linked to one and only one destination entity (\*-to-one link).
    In this case, if the current entity is updated,
    destination entities linked to the current updated entity are also updated.
    Likewise, if the current entity is created,
    a new destination entities linked to the current created entity is also created.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "CascadeCreateAndUpdate",
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

    params: CascadeCreateAndUpdateParams
    """
    CascadeCreateAndUpdate proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: CascadeCreateAndUpdateParams) -> CRUDableEntityTypeInterface:
        new_list_field = []
        for field in base_interface.fields.list_field:
            new_field = field.model_copy()
            if field.link is None:
                new_list_field.append(new_field)
            else:
                if field.link.type.dest.max == Cardinality.one:
                    #new_field.can_be_read = False#on ne lit pas la clé étrangère
                    #TODO : ne se répercute pas sur la requête SQL
                    new_list_field.append(new_field)
                    for linked_field in field.link.entity_type_linked_to.interface.fields.list_field:
                        if linked_field.name != field.link.field_name_linked_to:
                            new_field = linked_field.model_copy()
                            new_field.can_be_read = False#? faire un writable firewall
                            new_field.is_id_field = False#?
                            new_list_field.append(new_field)
                else:
                    raise NotImplementedError()
        base_interface.fields = Fields.build(new_list_field)
        return base_interface

    async def update(self, params: UpdateParams):
        """
        Scans all links of the entity type, and if the link has the correct cardinality, 
        updates the linked destination entities. 
        Then updates the current entity.
        """
        list_row = await self.read(
            ReadParams(
                transaction=params.transaction,
                list_filter_instance=[
                    FilterInstance(
                        field_name=field_name,
                        filter_value=params.dict_ids[field_name],
                        filtration_type=FilterationEnum.equal
                    )
                    for field_name in params.dict_ids
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
                    if field.link.type.dest.max == Cardinality.one and field.link.type.dest.min == Cardinality.one:
                        """
                        If the source is to be linked to a single destination,
                        then update the destination at the same time as the source
                        """
                        await field.link.entity_type_linked_to.update(
                            UpdateParams(
                                transaction=params.transaction, 
                                dict_ids={field.link.field_name_linked_to:row[field.name]}, 
                                dict_updator_value={
                                    k:v
                                    for k, v in params.dict_updator_value.items()
                                    if k in field.link.entity_type_linked_to.interface.fields.index_field_by_name
                                },
                                dict_updator_options=params.dict_updator_options
                            )
                        )
        return await self.base.update(
                    UpdateParams(
                        transaction=params.transaction, 
                        dict_ids=params.dict_ids, 
                        dict_updator_value={
                            k:v
                            for k, v in params.dict_updator_value.items()
                            if k in self.base.interface.fields.index_field_by_name
                        },
                        dict_updator_options=params.dict_updator_options
                    )
                )
    
    async def create(self, params: CreateParams):
        """
        Scans all links of the entity type, and if the link has the correct cardinality, 
        creates a linked destination entities. 
        Then creates the current entity.

        .. warning::
            Works only if the foreign key is specified in dict_creator_value.
        """
        await self.base.create(
            CreateParams(
                transaction=params.transaction, 
                dict_creator_value={
                    k:v
                    for k, v in params.dict_creator_value.items()
                    if k in self.base.interface.fields.index_field_by_name
                },
                dict_creator_options=params.dict_creator_options
            )
        )
        """list_row = self.read(
            transaction,
            [
                FilterInstance(
                    field_name=field_name,
                    filter_value=dict_creator_value[field_name],
                    filtration_type=FilterationEnum.equal
                )
                for field_name in dict_creator_value
                if field_name in self.base.interface.fields.index_field_by_name
            ],
            self.interface.get_readable_field_name())
        assert len(list_row) == 1#TODO : trouver une façon plus propre de récupérer la ligne qui vient d'être insérée
        """
        for field in self.interface.fields.list_field:
            if field.link is not None:
                if field.link.type.dest.max == Cardinality.one and field.link.type.dest.min == Cardinality.one:
                    """
                    If the source is to be linked to a single destination,
                    then the destination is created at the same time as the source
                    """
                    await field.link.entity_type_linked_to.create(
                        CreateParams(
                            transaction=params.transaction, 
                            dict_creator_value={
                                k:v
                                for k, v in params.dict_creator_value.items()
                                if k in field.link.entity_type_linked_to.interface.fields.index_field_by_name
                            } | {
                                field.link.field_name_linked_to:params.dict_creator_value[field.name]
                            },#must insert the key in the destination
                    #TODO : check upstream
                    dict_creator_options=params.dict_creator_options
                ))
    
    