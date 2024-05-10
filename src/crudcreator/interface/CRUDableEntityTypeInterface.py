from typing import Any
from pydantic import BaseModel, create_model
from ..Filter import FilterInstance, FilterType, FilterationEnum
from typing import Optional, Union, Literal
from ..OptionModel import OptionModel
from ..Sentinel import Sentinel

class CRUDableEntityTypeInterface(BaseModel):
    """
    Represents the schema of an entity type, i.e. what is visible to CRUD users on the entity.
    Performs no CRUD action as such.
    It's an empty shell.
    """
    
    name: str
    """
    The name of the entity type (e.g. "book").
    """

    fields: Optional[Union["Fields", Literal[Sentinel.unknown]]] = Sentinel.unknown
    """
    The fields that entities of this type will have.
    """

    can_indicate_read_distinct: bool
    """
    Can the user specify that only entities with a distinct value are to be read?
    """

    list_read_options: list[OptionModel] = []
    """
    Customizable options for crud actions (index name->type)
    """

    list_creator_options: list[OptionModel] = []
    """
    Customizable options for crud actions (index name->type)
    """

    list_updator_options: list[OptionModel] = []
    """
    Customizable options for crud actions (index name->type)
    """

    list_deletor_options: list[OptionModel] = []
    """
    Customizable options for crud actions (index name->type)
    """

    list_update_or_create_options: list[OptionModel] = []
    """
    Customizable options for crud actions (index name->type)
    """

    def get_sub_interface(self, name: str, list_field_name_to_keep: list[str]) -> "CRUDableEntityTypeInterface":
        """
        Creates and returns an interface identical to self,
        but contains only the list of fields to be retained.
        Gives a new name to the interface thus created.

        :param name:
            The name of the new interface.

        :param list_field_name_to_keep:
            The list of fields to keep.
        """
        return CRUDableEntityTypeInterface(
            **{
                **self.model_dump(),
                **{
                    "fields": Fields.build([
                        field for field in self.fields.list_field
                        if field.name in list_field_name_to_keep
                    ]),
                    "name": name
                }
            }
        )

    def get_readable_field(self) -> list["FieldOfCRUDableEntityType"]:
        """
        Returns the list of fields the user is allowed to read.
        """
        return [field for field in self.fields.list_field if field.can_be_read]
    
    def get_readable_field_name(self) -> list[str]:
        """
        Returns a list of field names that the user is authorized to read.
        """
        return [field.name for field in self.get_readable_field()]
    
    def get_fields_can_be_created(self) -> list["FieldOfCRUDableEntityType"]:
        """
        Returns the list of fields the user is allowed to write.
        """
        return [field for field in self.fields.list_field if field.can_be_created] 
    
    def get_fields_can_be_updated(self) -> list["FieldOfCRUDableEntityType"]:
        """
        Returns the list of fields that the user has the right to modify.
        """
        return [field for field in self.fields.list_field if field.can_be_updated] 
    
    def get_fields_can_be_updated_or_created(self) -> list["FieldOfCRUDableEntityType"]:
        """
        Returns the list of fields that the user has the right to modify or create.
        """
        return [field for field in self.fields.list_field if field.can_be_updated or field.can_be_created] 
    
    def get_filterable_field(self) -> list["FieldOfCRUDableEntityType"]:
        """
        Returns the list of fields on which the user has the right to filter.
        """
        return [field for field in self.fields.list_field if len(field.list_allowed_filter_type) > 0]
    
    def get_ids_field(self) -> list["FieldOfCRUDableEntityType"]:
        """
        Returns the list of fields used to uniquely identify an entity (entity identifiers).
        """
        return [field for field in self.fields.list_field if field.is_id_field]
    
    def _get_interface_filter_type_and_default(self, field: "FieldOfCRUDableEntityType", filter_type: FilterType) -> Any:
        type = field.type
        default = filter_type.default
        if not filter_type.is_mandatory:
            type = Optional[type]
        else:
            if default is None:
                default = ...
        return (type, default)
    
    def get_filter_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model for filters.

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        list_field = self.get_filterable_field()
        dict_field_type = {}
        for field in list_field:
            for allowed_filter_type in field.list_allowed_filter_type:
                dict_field_type[field.name+(
                    "" 
                    if len(field.list_allowed_filter_type) < 2 and not allowed_filter_type.force_long_name
                    else 
                    "_"+allowed_filter_type.filtration_type.value
                )] = self._get_interface_filter_type_and_default(field, allowed_filter_type)
        return create_model(
                f"{prefix}filter_on_object_{self.name}",
                **dict_field_type
            )
    
    def get_creator_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of expected data for an entity creation.

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}creator_of_{self.name}",
                **{
                   field.name:(field.type, field.default) 
                   for field in self.get_fields_can_be_created()
                }
            )
    
    def get_updator_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of the data expected for an entity update.
        
        :param prefix:
           A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}updator_of_{self.name}",
                **{
                   field.name:(field.type, None) 
                   for field in self.get_fields_can_be_updated()
                }
            )
    
    def get_update_or_create_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of the data expected for an entity "creation or update".
        
        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}update_or_create_of_{self.name}",
                **{
                   field.name:(field.type, field.default)#tout est obligatoire dans un update_or_create (put) 
                   for field in self.get_fields_can_be_updated_or_created()
                }
            )
    
    def get_ids_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of the data expected to identify a single entity.

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}ids_of_{self.name}",
                **{
                   field.name:(field.type, field.default) 
                   for field in self.get_ids_field()
                }
            )
    
    def get_read_response_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of the entities returned by a read.
        
        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
            f"{prefix}{self.name}",
            **{
                crud_field.name:(
                    crud_field.get_interface_read_type(),
                    crud_field.get_interface_read_default()
                )
                for crud_field in self.get_readable_field()
            }
        )
    
    def get_read_options_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of entity reading options.

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}read_option_of_{self.name}",
                **{
                   option.name:self._get_interface_filter_type_and_default(option, option)#TODO : une fonction pour les options, ou sinon une fonction pour les deux
                   for option in self.list_read_options
                }
            )
    
    def get_create_options_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of options for an entity creation.

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}creator_option_of_{self.name}",
                **{
                   option.name:(option.type, option.default) 
                   for option in self.list_creator_options
                }
            )
    
    def get_update_options_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of options for an entity update.

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}updator_option_of_{self.name}",
                **{
                   option.name:(option.type, option.default) 
                   for option in self.list_updator_options
                }
            )
    
    def get_delete_options_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of options for an entity suppression.
        
        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}deletor_option_of_{self.name}",
                **{
                   option.name:(option.type, option.default) 
                   for option in self.list_deletor_options
                }
            )
    
    def get_update_or_create_options_data_model(self, prefix: str = "") -> BaseModel:
        """
        Returns the Pydantic model of options for an entity "creation or modification".

        :param prefix:
            A prefix to be added to the Pydantic model name to make it unique (necessary for swagger
            REST APIs, for example)
        """
        return create_model(
                f"{prefix}update_or_create_option_of_{self.name}",
                **{
                   option.name:(option.type, option.default) 
                   for option in self.list_update_or_create_options
                }
            )
    
from ..FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ..Fields import Fields
CRUDableEntityTypeInterface.model_rebuild()