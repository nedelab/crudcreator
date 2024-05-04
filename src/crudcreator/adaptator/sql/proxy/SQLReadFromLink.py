from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ....Sentinel import Sentinel
from ....proxy.AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from ....AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Fields import Fields
from ....FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ....Filter import FilterInstance
from enum import Enum
from ....Link import Link
from .AbstractSQLRequestProxy import AbstractSQLRequestProxy, AbstractSQLRequestProxyParams
from sqlalchemy.sql import Select, Delete, Insert, Update
from ....proxy.AbstractProxyParams import AbstractProxyParams
from ..SQLColumnInspector import SQLColumnInspector
from ....interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ....LinkType import LinkType, Cardinality
from ....transaction.sql.SQLTransaction import SQLTransaction
from ....schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools

class SQLActivateEntityOnlyOnOption(BaseModel):
    """
    Represents a "join" activated only on option.
    """

    entity_name: str
    """
    Entity type to "join" only on option.
    """

    option_name: str
    """
    The option that activates the "join" function
    """

class SQLReadFromLinkParams(AbstractSQLRequestProxyParams):
    """
    SQLReadFromLink proxy parameters.
    """

    list_activate_entity_only_on_option: list[SQLActivateEntityOnlyOnOption] = []
    """
    It is possible to activate the "join" option only.
    """
    
    @functools.cached_property
    def index_activate_entity_only_on_option(self) -> dict[str, bool]:
        """
        Index entity_name->option_name built automatically from list_activate_entity_only_on_option.
        """
        return {k.entity_name:k.option_name for k in self.list_activate_entity_only_on_option}

class SQLReadFromLink(AbstractSQLRequestProxy):
    """
    Transforms links present in the interface into "joins" in the SQL query.

    Example of descriptor :

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SQLReadFromLink",
            "params": {}
        }
    """

    params: SQLReadFromLinkParams
    """
    SQLReadFromLink proxy parameters.
    """

    @staticmethod
    def _get_not_ambiguous_name(
            list_existing_field_name: list[str],
            old_field: FieldOfCRUDableEntityType, 
            new_field: FieldOfCRUDableEntityType
    ) -> str:
        if new_field.name in list_existing_field_name:
            return f"{old_field.link.entity_type_linked_to.interface.name}.{new_field.name}"
        else:
            return new_field.name

    @classmethod
    def _get_updated_interface(cls, base_interface: CRUDableEntityTypeInterface, params: SQLReadFromLinkParams) -> CRUDableEntityTypeInterface:
        new_list_field = []
        for field in base_interface.fields.list_field:
            #we first run through the entity's fields, so that they come first.
            #if field.link is None:
            new_list_field.append(field.model_copy())
        cls._get_updated_interface_rec(base_interface.fields.list_field, new_list_field, params)
        base_interface.fields = Fields.build(new_list_field)
        return base_interface
    @classmethod
    def _get_updated_interface_rec(
        cls, 
        list_field:  list[FieldOfCRUDableEntityType],  
        new_list_field: list[FieldOfCRUDableEntityType], 
        params: SQLReadFromLinkParams
    ) -> CRUDableEntityTypeInterface:
        for field in list_field:
             #then we browse the related fields
             if field.link is not None:
                #if field.link.type.dest.max == Cardinality.one:
                #new_field.can_be_read = False#the foreign key is not read
                #TODO : does not affect the SQL query
                #the presentation layer takes place after SQL (in particular many-to-many aggregation)
                #new_list_field.append(field.model_copy())
                for linked_field in field.link.entity_type_linked_to.interface.fields.list_field:
                    """if (
                        linked_field.name != field.link.field_name_linked_to or
                        field.link.type.dest.min == Cardinality.zero#si outer join, on garde la clé 
                        #étrangère de la table destination, pour distinguer entre une ligne de la 
                        #table destination avec que des null, et une ligne inexistante
                    ):"""
                    new_field = linked_field.model_copy()
                    new_field.can_be_created = False#? do a writable firewall
                    new_field.can_be_updated = False#? do a writable firewall
                    new_field.is_id_field = False
                    new_field.name = cls._get_not_ambiguous_name([field.name for field in new_list_field], field, new_field)
                    if field.link.entity_type_linked_to.interface.name in params.index_activate_entity_only_on_option:
                        new_field.type = Optional[new_field.type]
                    new_list_field.append(new_field)
                #new_field = field.model_copy()
                #new_field.link = None#the link is read, shall we remove it?
                cls._get_updated_interface_rec(field.link.entity_type_linked_to.interface.fields.list_field, new_list_field, params)
                #else:
                #    raise NotImplementedError()

    async def read(self, params: ReadParams) -> Select:
        """
        Retrieves the select from the next proxy, then adds the necessary "join".
        """
        #TODO : link within a link (if the linked entity already has a link)
        req = await self.base.read(params)
        req = await self._read_rec(
            req, 
            self.base.interface.fields.list_field, 
            list(self.base.interface.fields.index_field_by_name.keys()), 
            params,
            await self.get_inspector()
        )
        return req
    
    async def _read_rec(
        self, 
        req: Select,
        list_field:  list[FieldOfCRUDableEntityType], 
        list_field_name_done:  list[str],
        params: ReadParams,
        inspector: SQLColumnInspector,
    ) -> Select:
        #TODO : ajouter join seulement si un champ de la table dans la liste des lectures, ou des filtres, ou des sorts, etc
        for field in list_field:
            if (
                field.link is not None and
                (
                    field.link.entity_type_linked_to.interface.name not in self.params.index_activate_entity_only_on_option or
                    params.dict_read_options.get(self.params.index_activate_entity_only_on_option[field.link.entity_type_linked_to.interface.name], False) == True
                )
            ):
                linked_crud_object: AbstractSQLRequestProxy = field.link.entity_type_linked_to
                req = req.join(
                    (await linked_crud_object.get_inspector()).table,
                    (await linked_crud_object.get_inspector()).index_sqlalchemy_column[field.link.field_name_linked_to] == inspector.index_sqlalchemy_column[field.name],
                    isouter=(field.link.type.dest.min == Cardinality.zero)#outer join si possiblement 0 destination
                )
        
                for linked_field in field.link.entity_type_linked_to.interface.fields.list_field:
                    """if (
                        linked_field.name != field.link.field_name_linked_to or
                        field.link.type.dest.min == Cardinality.zero#si outer join, on garde la clé 
                        #étrangère de la table destination, pour distinguer entre une ligne de la 
                        #table destination avec que des null, et une ligne inexistante
                    ):"""
                    if linked_field.name in params.list_read_field:
                        req = req.add_columns(
                            (await linked_crud_object.get_inspector())
                            .index_sqlalchemy_column[linked_field.name]
                            .label(self.__class__._get_not_ambiguous_name(list_field_name_done, field, linked_field))
                        )
                        list_field_name_done.append(self.__class__._get_not_ambiguous_name(list_field_name_done, field, linked_field))
                req = await self._read_rec(
                    req, 
                    field.link.entity_type_linked_to.interface.fields.list_field, 
                    list_field_name_done, 
                    params,
                    await field.link.entity_type_linked_to.get_inspector()
                )
        return req

    
    