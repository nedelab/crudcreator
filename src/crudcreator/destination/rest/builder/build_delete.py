from fastapi import APIRouter, Depends, HTTPException, status, params
from ....exceptions import EntityNotExist, EntityAlreadyExist
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from typing import Optional, Callable, Tuple, Any
from ..ErrorModel import ErrorModel
from ....Filter import FilterInstance, FilterType, FilterationEnum
from ....transaction.AbstractTransactionManager import AbstractTransactionManager
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
from .base import _BaseRESTCRUDBuilder, FieldTypeToSplit

class _DeleteRESTCRUDBuilder(_BaseRESTCRUDBuilder):

    def build_delete(
            self, 
            entity_type: AbstractCRUDableEntityType, 
            transaction_manager: AbstractTransactionManager,
            ids_from_dependencies: dict[str, params.Depends] = {}
        ):
        """
        Adds a DELETE route to the router to delete an entity.
        
        :param entity_type:
            The type of entity on which to plug the destination interface.

        :param transaction_manager:
            The manager that will handle all transactional matters.

        :param ids_from_dependencies:
            A dictionary associating a dependency with an id (which will not be provided
            by the API user). For example, a dependency that reads
            a jwt token and returns the username of the user calling the route (for example, to restrict
            delete to entities over which the user has rights).

        """

        #le modèle pydantic des options de la route
        option_model = entity_type.interface.get_delete_options_data_model()

        #on sépare les ids à récupérer en deux modèles
        #les ids permettent d'identifier l'entité à supprimer
        deletor_data_model, deletor_data_model_from_dependencies = self._split_for_dependencies(
            entity_type,
            FieldTypeToSplit.ids,
            ids_from_dependencies, 
            "ids_deletor"
        )

        #on construit la route
        @self.router.delete(
                    f"/{entity_type.interface.name}",
                    tags=self._get_tags(entity_type),
                    description=f"""
Delete a {entity_type.interface.name}.
                    """,
                    responses={
                        404: {#si l'entité que l'utilisateur veut supprimer n'existe pas (aucune entité avec les ids spécifiés)
                            "model": ErrorModel
                        }
                    }
            )
        async def route(
            deletor_value: deletor_data_model = Depends(),
            options: option_model = Depends(),
            deletor_value_from_dependencies = Depends(deletor_data_model_from_dependencies),
        ):
            
            #on fusionne les dictionnaires d'id donnés en paramètre par FastAPI
            deletor_value = deletor_value.model_dump() | deletor_value_from_dependencies.model_dump()

            try:
                async with transaction_manager.begin() as transaction:
                    await entity_type.delete(
                        DeleteParams(
                            transaction=transaction, 
                            dict_deletor_value=deletor_value,
                            dict_deletor_options=options.model_dump()
                        )
                    )
            except EntityNotExist:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail="The entity does not exist"
                )