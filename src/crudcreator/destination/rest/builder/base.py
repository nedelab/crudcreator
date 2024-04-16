from fastapi import APIRouter, Depends, HTTPException, status, params
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ...AbstractDestinationCRUDBuilder import AbstractDestinationCRUDBuilder
from typing import Tuple, Any, Callable
from ....Fields import Fields
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from pydantic import BaseModel
from enum import Enum

class FieldTypeToSplit(Enum):
    ids: str = "ids"
    update_or_create: str = "update_or_create"
    
class _BaseRESTCRUDBuilder(AbstractDestinationCRUDBuilder):

    def __init__(self, index_filter_override: dict[str, Tuple[Any, Callable]]):
        self.router = APIRouter()
        self.index_filter_override = index_filter_override#TODO : encore utile ?

    def get_built_router(self) -> APIRouter:
        """
        Returns the built FastAPI router.
        """
        return self.router

    def _get_tags(self, entity_type: AbstractCRUDableEntityType) -> str:
        """
        Returns the tags to associate with an entity's routes in the swagger.
        Today, it returns only one tag, which is the name of the entity.
        """
        return [
            entity_type.interface.name.replace("_", " ").upper()
        ]
    
    def _split_for_dependencies(
        self, 
        entity_type: AbstractCRUDableEntityType, 
        field_type_to_split: FieldTypeToSplit,
        dict_dependencies: dict[str, params.Depends],
        model_key: str,
    ) -> tuple[BaseModel, BaseModel]:
        """
        Separates entity fields into two categories: those that will be filled in directly by the
        Rest API user, and those that will be filled by a FastAPI dependency.
        Returns the pydantic model for both categories.
        """
        if field_type_to_split == FieldTypeToSplit.ids:
            list_fields_to_split = entity_type.interface.get_ids_field()
        elif field_type_to_split == FieldTypeToSplit.update_or_create:
            list_fields_to_split = entity_type.interface.get_fields_can_be_updated_or_created()
        else:
            raise NotImplementedError()

        interface = entity_type.interface.get_sub_interface(
            f"submodel_{model_key}_{entity_type.interface.name}",
            [field.name for field in list_fields_to_split if field.name not in dict_dependencies]
        )

        interface_from_dependencies = entity_type.interface.get_sub_interface(
            f"submodel_{model_key}_from_dependencies_{entity_type.interface.name}",
            [field.name for field in list_fields_to_split if field.name in dict_dependencies]
        )
        list_new_field = []
        for field in interface_from_dependencies.fields.list_field:
            new_field = field.model_copy()
            new_field.default = dict_dependencies[new_field.name]#TODO : supprime aussi la valeur par défaut du filtre
            list_new_field.append(new_field)
        interface_from_dependencies.fields = Fields.build(list_new_field)

       

        if field_type_to_split == FieldTypeToSplit.ids:
            model = interface.get_ids_data_model()
            model_from_dependencies = interface_from_dependencies.get_ids_data_model()
        elif field_type_to_split == FieldTypeToSplit.update_or_create:
            model = interface.get_update_or_create_data_model()
            model_from_dependencies = interface_from_dependencies.get_update_or_create_data_model()
        else:
            raise NotImplementedError()

        return model, model_from_dependencies

   