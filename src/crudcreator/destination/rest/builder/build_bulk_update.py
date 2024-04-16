from fastapi import APIRouter, Depends, HTTPException, status, params
from ....exceptions import EntityNotExist, EntityAlreadyExist
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from pydantic import create_model, BaseModel, ConfigDict
from ..BulkErrorModel import BulkErrorModel, _BulkErrorModel
from ....transaction.AbstractTransactionManager import AbstractTransactionManager
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
import inspect
from .base import _BaseRESTCRUDBuilder, FieldTypeToSplit
from ....Fields import Fields

class _BulkUpdateRESTCRUDBuilder(_BaseRESTCRUDBuilder):

    def build_bulk_update(
        self, 
        entity_type: AbstractCRUDableEntityType, 
        transaction_manager: AbstractTransactionManager,
        ids_from_dependencies: dict[str, params.Depends] = {}
    ):
        """
        Adds a PATCH route to the router to modify multiple entities.

        :param entity_type:
            The type of entity on which to plug the destination interface.

        :param transaction_manager:
            The manager that will handle all transactional matters.
        
        :param ids_from_dependencies:
            A dictionary associating a dependency with an id (which will not be provided
            by the API user). For example, a dependency that reads
            a jwt token and returns the username of the user calling the route (for example, to restrict
            update to entities over which the user has rights).

        TODO: make a generic build_bulk that builds what's needed for update, create and delete.
        """

        ids_data_model, ids_model_from_dependencies = self._split_for_dependencies(
            entity_type, 
            FieldTypeToSplit.ids,
            ids_from_dependencies, 
            "ids_bulk_updator"
        )

        bulk_updator_model = create_model(
                f"bulk_updator_of_{entity_type.interface.name}",
                ids=(ids_data_model, ...),
                fields_to_update=(entity_type.interface.get_updator_data_model("bulk_data_"), ...),
                options=(entity_type.interface.get_update_options_data_model("bulk_"), ...)
            )

        @self.router.patch(
                    f"/{entity_type.interface.name}/bulk",
                    tags=self._get_tags(entity_type),
                    description=f"""
Update several {entity_type.interface.name} in an atomic way.
                    """,
                    responses={
                        400: {
                            "model": BulkErrorModel
                        }
                    }
            )
        async def route(
            list_updator_value: list[bulk_updator_model],
            ids_from_dependencies = Depends(ids_model_from_dependencies)
        ):
            list_error = []
            async with transaction_manager.begin() as transaction:
                for updator_value in list_updator_value:
                    try:
                        await entity_type.update(
                            UpdateParams(
                                transaction=transaction, 
                                dict_ids=(updator_value.ids.model_dump()|ids_from_dependencies.model_dump()), 
                                dict_updator_value=updator_value.fields_to_update.model_dump(),
                                dict_updator_options=updator_value.options.model_dump()
                            )
                        )
                    except EntityAlreadyExist:
                        list_error.append(
                            _BulkErrorModel(
                                http_status=status.HTTP_409_CONFLICT,
                                detail=f"The ids {updator_value.ids.model_dump()} are already in use by another entity"
                            ).model_dump()
                        )
                    except EntityNotExist:
                        list_error.append(
                            _BulkErrorModel(
                                http_status=status.HTTP_404_NOT_FOUND,
                                detail=f"The entity {updator_value.ids.model_dump()} does not exist"
                            ).model_dump()
                        )
                if len(list_error) > 0:#le faire avant la sortie de la transaction, pour rollback
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST,
                        detail=list_error
                    )