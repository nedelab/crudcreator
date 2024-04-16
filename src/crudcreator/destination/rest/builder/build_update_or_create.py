from fastapi import APIRouter, Depends, HTTPException, status, params
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....transaction.AbstractTransactionManager import AbstractTransactionManager
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
import inspect
from .base import _BaseRESTCRUDBuilder, FieldTypeToSplit
from ....exceptions import EntityNotExist, EntityAlreadyExist
from ..ErrorModel import ErrorModel

class _UpdateOrCreateRESTCRUDBuilder(_BaseRESTCRUDBuilder):

    def build_update_or_create(
        self, 
        entity_type: AbstractCRUDableEntityType, 
        transaction_manager: AbstractTransactionManager,
        ids_from_dependencies: dict[str, params.Depends] = {},
        values_from_dependencies: dict[str, params.Depends] = {}
    ):
        """
        Adds a PUT route to the router to add an entity if it doesn't exist, or modify it if it does.
        
        :param entity_type:
            The entity type on which to plug the destination interface.

        :param transaction_manager:
            The manager that will handle all transactional matters.

        :param ids_from_dependencies:
            A dictionary associating a dependency with an id (which will not be provided
            by the API user). For example, a dependency that reads
            a jwt token and returns the username of the user calling the route (for example, to restrict
            update to entities over which the user has rights).

        :param values_from_dependencies:
            A dictionary associating a dependency with a value (which will then not be provided
            by the API user). For example, a dependency that reads
            a jwt token and returns the username of the user calling the route (for example, to add
            the name of the user who is using the API to the entity it creates).

        """

        #on sépare les ids à récupérer en deux modèles
        #les ids permettent d'identifier l'entité à créer ou modifier
        ids_data_model, ids_model_from_dependencies = self._split_for_dependencies(
            entity_type,
            FieldTypeToSplit.ids,
            ids_from_dependencies, 
            "ids_update_or_create"
        )

        #on sépare les valeurs à récupérer en deux modèles
        update_or_create_data_model, update_or_create_data_model_from_dependencies = self._split_for_dependencies(
            entity_type,
            FieldTypeToSplit.update_or_create,
            values_from_dependencies, 
            "value_update_or_create"
        )

        #le modèle pydantic des options de la route
        option_model = entity_type.interface.get_update_or_create_options_data_model()

        #on construit la route
        @self.router.put(
                    f"/{entity_type.interface.name}",
                    tags=self._get_tags(entity_type),
                    description=f"""
Create or update a {entity_type.interface.name}.
                    """,
                    responses={
                        409: {#si l'entité que l'utilisateur veut construire existe déjà (une entité avec les mêmes ids existent déjà)
                            "model": ErrorModel
                        }
                    }
            )
        async def route(
            update_or_create_value: update_or_create_data_model,
            update_or_create_value_from_dependencies = Depends(update_or_create_data_model_from_dependencies),
            ids: ids_data_model = Depends(),
            ids_from_dependencies = Depends(ids_model_from_dependencies),
            options: option_model = Depends()
        ):
            #on fusionne les dictionnaires d'ids et de valeurs donnés en paramètre par FastAPI
            ids = ids.model_dump() | ids_from_dependencies.model_dump()
            update_or_create_value = update_or_create_value.model_dump() | update_or_create_value_from_dependencies.model_dump()

            try:
                await entity_type.update_or_create(
                    UpdateOrCreateParams(
                        transaction_manager=transaction_manager,
                        dict_ids=ids,
                        dict_update_or_create_value=update_or_create_value,
                        dict_update_or_create_options=options.model_dump()
                    )
                )
            except EntityAlreadyExist:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    detail="The ids are already in use by another entity"
                )
