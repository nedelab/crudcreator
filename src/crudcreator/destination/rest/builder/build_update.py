from fastapi import APIRouter, Depends, HTTPException, status, params
from ....exceptions import EntityNotExist, EntityAlreadyExist
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ..ErrorModel import ErrorModel
from ....transaction.AbstractTransactionManager import AbstractTransactionManager
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
import inspect
from .base import _BaseRESTCRUDBuilder, FieldTypeToSplit
from ....Fields import Fields

class _UpdateRESTCRUDBuilder(_BaseRESTCRUDBuilder):

    def build_update(
        self, 
        entity_type: AbstractCRUDableEntityType, 
        transaction_manager: AbstractTransactionManager,
        ids_from_dependencies: dict[str, params.Depends] = {}
    ):
        """
        Adds a PATCH route to the router to modify an entity.

        :param entity_type:
            The type of entity on which to plug the destination interface.

        :param transaction_manager:
            The manager that will handle all transactional matters.

        :param ids_from_dependencies:
            A dictionary associating a dependency with an id (which will not be provided
            by the API user). For example, a dependency that reads
            a jwt token and returns the username of the user calling the route (for example, to restrict
            update to entities over which the user has rights).
        
        """

        #le modèle pydantic des champs à modifier
        updator_data_model = entity_type.interface.get_updator_data_model()

        #le modèle pydantic des options de la route
        option_model = entity_type.interface.get_update_options_data_model()

        #on sépare les ids à récupérer en deux modèles
        #les ids permettent d'identifier l'entité à modifier
        ids_data_model, ids_model_from_dependencies = self._split_for_dependencies(
            entity_type,
            FieldTypeToSplit.ids,
            ids_from_dependencies, 
            "ids_updator"
        )

        #on construit la route
        @self.router.patch(
                    f"/{entity_type.interface.name}",
                    tags=self._get_tags(entity_type),
                    description=f"""
Update a {entity_type.interface.name}.
                    """,
                    responses={
                        409: {#si l'entité que l'utilisateur veut construire existe déjà (une entité avec les mêmes ids existent déjà)
                            "model": ErrorModel
                        },
                        
                        404: {#si l'entité que l'utilisateur veut modifier n'existe pas (aucune entité avec les ids spécifiés)
                            "model": ErrorModel
                        }
                    }
            )
        async def route(
            updator_value: updator_data_model,
            ids: ids_data_model = Depends(),
            ids_from_dependencies = Depends(ids_model_from_dependencies),
            options: option_model = Depends()
        ):
            
            #on fusionne les dictionnaires d'id donnés en paramètre par FastAPI
            ids = ids.model_dump() | ids_from_dependencies.model_dump()
            
            try:
                async with transaction_manager.begin() as transaction:
                    await entity_type.update(
                        UpdateParams(
                            transaction=transaction, 
                            dict_ids=ids, 
                            dict_updator_value=updator_value.model_dump(),
                            dict_updator_options=options.model_dump()
                        )
                    )
            except EntityAlreadyExist:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    detail="The ids are already in use by another entity"
                )
            except EntityNotExist:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail="The entity does not exist"
                )
         