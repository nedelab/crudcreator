from fastapi import APIRouter, Depends, HTTPException, status, params
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....Fields import Fields
from ....Filter import FilterInstance, FilterType, FilterationEnum
from ....transaction.AbstractTransactionManager import AbstractTransactionManager
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams, UpdateOrCreateParams
import inspect
from .base import _BaseRESTCRUDBuilder

class _ReadRESTCRUDBuilder(_BaseRESTCRUDBuilder):

    def build_read(
        self, 
        entity_type: AbstractCRUDableEntityType, 
        transaction_manager: AbstractTransactionManager,
        filter_from_dependencies: dict[str, params.Depends] = {}
    ):
        """
        Adds a GET route to the router to read a list of entities.

        :param entity_type:
            The type of entity on which to plug the destination interface.

        :param transaction_manager:
            The manager that will handle all transactional matters.

        :param filter_from_dependencies:
            A dictionary associating a dependency with a filter (which will not be provided
            directly by the API user).

        """

        #le model pydantic des filtres renseignés directement par l'utilisateur de l'API
        filter_data_model = entity_type.interface.get_sub_interface(
            f"submodel_filter_{entity_type.interface.name}",
            [field.name for field in entity_type.interface.get_filterable_field() if field.name not in filter_from_dependencies]
        ).get_filter_data_model(entity_type)

        #le model pydantic des filtres renseignés par dépendance FastAPI
        filter_data_interface_from_dependencies = entity_type.interface.get_sub_interface(
            f"submodel_filter_from_dependencies_{entity_type.interface.name}",
            [field.name for field in entity_type.interface.get_filterable_field() if field.name in filter_from_dependencies]
        )
        list_new_field = []
        for field in filter_data_interface_from_dependencies.fields.list_field:
            new_field = field.model_copy()
            new_field.list_allowed_filter_type = [
                FilterType(
                    **(allower_filter_type.model_dump() | {"default": filter_from_dependencies[new_field.name]})
                )
                for allower_filter_type in new_field.list_allowed_filter_type
                
            ]#TODO : ne fonctionne que si un seul filtre sur le champ
            #TODO : supprime aussi la valeur par défaut du filtre
            list_new_field.append(new_field)
        filter_data_interface_from_dependencies.fields = Fields.build(list_new_field)
        filter_data_model_from_dependencies = filter_data_interface_from_dependencies.get_filter_data_model()
        
        #le model pydantic de la réponse de l'API
        response_model = entity_type.interface.get_read_response_data_model()

        #le modèle pydantic des options de la route
        option_model = entity_type.interface.get_read_options_data_model()

        list_crud_field_filter = entity_type.interface.get_filterable_field()
        list_readable_field_name = [
            field.name
            for field in entity_type.interface.get_readable_field()
        ]#en REST, on lit tous les champs

        #on construit la description des filtres de la route
        description_possible_filter = ""
        if len(list_crud_field_filter) > 0:
            description_filter_list = "\n\n".join([
                f"* {crud_field.name} ({', '.join([filter_type.filtration_type.value for filter_type in crud_field.list_allowed_filter_type])})"
                for crud_field in list_crud_field_filter
                if crud_field.name not in self.index_filter_override
            ])
            description_possible_filter = f"""Possible filters :

{description_filter_list}
"""
        
        
        #on construit la route
        @self.router.get(
                f"/{entity_type.interface.name}",
                tags=self._get_tags(entity_type),
                response_model=list[response_model],
                description=f"""
Return a list of {entity_type.interface.name}.

{description_possible_filter}
                    """
                )
        async def route(
            filter: filter_data_model = Depends(),
            options: option_model = Depends(),
            filter_from_dependencies = Depends(filter_data_model_from_dependencies)
        ):   
            #on fusionne les dictionnaires de filtre donnés en paramètre par FastAPI
            filter_data = filter.model_dump() | filter_from_dependencies.model_dump()

            #on construit la liste des instances de filtre (qui sera passée à l'entité)
            list_filter_instance = []
            for field in list_crud_field_filter:
                for filter_type in field.list_allowed_filter_type:
                    #on récupère la valeur du filtre dans le dictionnaire donné en paramètre par FastAPI
                    v = filter_data[field.name+(
                        "" 
                        if len(field.list_allowed_filter_type) < 2 and not filter_type.force_long_name
                        else 
                        "_"+filter_type.filtration_type.value
                    )]
                    if v is not None:#s'il y a un filtre (TODO : mettre une sentinelle pour autoriser les filtres sur "null")
                        list_filter_instance.append(
                        FilterInstance(
                                field_name=field.name,
                                filter_value=v,
                                filtration_type=filter_type.filtration_type
                            ) 
                        )

            async with transaction_manager.begin() as transaction:
                #on envoie le tout à l'entité qui s'occupe du reste
                return await entity_type.read(
                    ReadParams(
                        transaction=transaction, 
                        list_filter_instance=list_filter_instance, 
                        list_read_field=list_readable_field_name,
                        dict_read_options=options.model_dump()
                    )
                )