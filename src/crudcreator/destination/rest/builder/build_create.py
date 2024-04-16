from fastapi import APIRouter, Depends, HTTPException, status, params
from ....exceptions import EntityNotExist, EntityAlreadyExist
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from typing import Optional, Callable, Tuple, Any
from ..ErrorModel import ErrorModel
from ....transaction.AbstractTransactionManager import AbstractTransactionManager
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
import inspect
from .base import _BaseRESTCRUDBuilder

class _CreateRESTCRUDBuilder(_BaseRESTCRUDBuilder):
        
    def build_create(
        self, 
        entity_type: AbstractCRUDableEntityType, 
        transaction_manager: AbstractTransactionManager
    ):
        """
        Adds a POST route to the router to create an entity.

        :param entity_type:
            The type of entity on which to plug the destination interface.

        :param transaction_manager:
            The manager that will handle all transactional matters.

        """
        #TODO : check is_id_field unique

        #le modèle pydantic des champs attendus pour la création d'une entité
        creator_data_model = entity_type.interface.get_creator_data_model()

        #le modèle pydantic des options de la route
        option_model = entity_type.interface.get_create_options_data_model()

        #on construit la route
        @self.router.post(
                    f"/{entity_type.interface.name}",
                    tags=self._get_tags(entity_type),
                    description=f"""
Create a {entity_type.interface.name}.
                    """,
                    responses={
                        409: {#si l'entité que l'utilisateur veut construire existe déjà (une entité avec les mêmes ids existent déjà)
                            "model": ErrorModel
                        }
                    }
            )
        async def route(
            creator_value: creator_data_model,
            options: option_model = Depends()
        ):
            try: 
                async with transaction_manager.begin() as transaction:
                    await entity_type.create(
                        CreateParams(
                            transaction=transaction, 
                            dict_creator_value=creator_value.model_dump(),
                            dict_creator_options=options.model_dump()
                        )
                    )
            except EntityAlreadyExist:
                raise HTTPException(
                    status.HTTP_409_CONFLICT,
                    detail="The ids are already in use by another entity"
                )

