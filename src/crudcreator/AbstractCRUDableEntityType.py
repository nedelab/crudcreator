from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional, ForwardRef, TYPE_CHECKING
from .Sentinel import Sentinel
from .Filter import FilterInstance, FilterType, FilterationEnum
from contextlib import contextmanager
from .transaction.AbstractTransaction import AbstractTransaction
from .schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
from .exceptions import EntityAlreadyExist

class AbstractCRUDableEntityType(BaseModel):
    """
    An instance of this class represents a CRUDable entity type. This is CRUDCreator's main class.
    Proxies and source modules inherit from this class.
    See :ref:`how_does_it_work`.
    """

    interface: "CRUDableEntityTypeInterface"
    """
    The interface/schema of the entity type, as seen by the entity's CRUD users.
    """

    """class Config():
        copy_on_model_validation = "none"
    """#TODO : removed in v2, vérifier les conséquences

    #les actions CRUD
    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        Returns a list of entities.
        Entities are returned as dictionaries, whose keys are the entity's attributes.

        :param params:
            CRUD **read** query parameters.
        """
        raise NotImplementedError()
    
    async def create(self, params: CreateParams):
        """
        Creates an entity.

        :param params:
            CRUD query parameters **create**.
        """
        raise NotImplementedError()
    
    async def delete(self, params: DeleteParams):
        """
        Deletes an entity.

        :param params:
            CRUD **delete** query parameters.
        """
        raise NotImplementedError()
    
    async def update(self, params: UpdateParams):
        """
        Updates an entity.

        :param params:
            CRUD query parameters **update**.
        """
        raise NotImplementedError()
    
    async def update_or_create(self, params: UpdateOrCreateParams):
        """
        Creates an entity if it doesn't exist, updates it if it does.

        :param params:
            CRUD query parameters **update_or_create**.
        """
        try:
            async with params.transaction_manager.begin() as transaction:
                return await self.create(
                    CreateParams(
                        transaction=transaction, 
                        dict_creator_value={k:v for k,v in params.dict_update_or_create_value.items() if self.interface.fields.index_field_by_name[k].can_be_created},
                        dict_creator_options=params.dict_update_or_create_options
                    )   
                )
        except EntityAlreadyExist:
            async with params.transaction_manager.begin() as transaction:
                return await self.update(
                    UpdateParams(
                        transaction=transaction, 
                        dict_ids=params.dict_ids, 
                        dict_updator_value={k:v for k,v in params.dict_update_or_create_value.items() if self.interface.fields.index_field_by_name[k].can_be_updated},
                        dict_updator_options=params.dict_update_or_create_options
                    )
                )
            
    
    async def check_integrity(
        self, 
        transaction: AbstractTransaction, 
        dict_value_new_entity: dict[str, Any]
    ):
        """
        Used to check that a hypothetical entity, represented by dict_value_new_entity, would not
        violate any integrity constraints if created.

        :param transaction:
            The current transaction

        :param dict_value_new_entity:
            A **field name** -> value dictionary. Represents the fields of the new entity which we want to check
            that it will not violate integrity constraints if created.

            .. warning::
                Must therefore include at least all ids fields that are not automatically generated.

            .. warning::
                All mandatory filter fields must also be present in dict_value_new_entity.
                Otherwise, there's a risk that a proxy read will crash, because it was expecting a filter that isn't there.

        :raises EntityAlreadyExist:
            If the creation of an entity with "dict_value_new_entity" values
            would violate the ids uniqueness constraint.

        """
        list_ids_field = self.interface.get_ids_field()
        list_filter_on_id = []
        should_manually_very_integrity = True
        for field in list_ids_field:
            #on constitue les filtres qu'il faudra faire si l'on doit vérifier manuellement l'unicité
            if field.name not in dict_value_new_entity and field.is_automatically_generated:
                #alors il n'y aura pas de pb d'intégrité, on peut s'arrêter là (gagne du temps)
                should_manually_very_integrity = False
                break
            elif field.name not in dict_value_new_entity and not field.is_automatically_generated:
                #TODO : vérifier que field.default ne peut être null ?
                #TODO : laisser les couches d'après rajouter la valeur par défaut ?
                list_filter_on_id.append(
                    FilterInstance(
                        field_name=field.name,
                        filter_value=field.default,
                        filtration_type=FilterationEnum.equal
                    )
                )
            else:
                list_filter_on_id.append(
                    FilterInstance(
                        field_name=field.name,
                        filter_value=dict_value_new_entity[field.name],
                        filtration_type=FilterationEnum.equal
                    )
                )

        if should_manually_very_integrity:
            if len(
                await self.read(
                    ReadParams(
                        transaction=transaction, 
                        list_filter_instance=list_filter_on_id, 
                        list_read_field=self.interface.get_readable_field_name(),#TODO : bloqué s'il y a un champ dans la liste à updater qui n'est pas readable
                        dict_read_options={},
                        limit=1,
                        offset=None,
                        must_read_distinct=False,
                        list_field_on_which_to_sort=[]
                    )
                )
            ) > 0:
                raise EntityAlreadyExist()
    

    
from .interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
AbstractCRUDableEntityType.model_rebuild()