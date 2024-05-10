


from pydantic import BaseModel, validator
from .LinkType import LinkType
from typing import Optional, ForwardRef, TYPE_CHECKING

class Link(BaseModel):
    """
    Represents a link to an entity type.
    """

    entity_type_linked_to: "AbstractCRUDableEntityType"
    """
    The type of entity to which the link is pointing.
    """

    field_name_linked_to: str
    """
    The field of the destination entity through which the link is made.
    """

    type: Optional[LinkType] = None
    """
    Link cardinality.
    """

class LinkedField(BaseModel):
    field_name: str
    """
    The name of the current entity type's field to which the link is made.
    """

    link: Link
    """
    The link.
    """

class LinkToSource(BaseModel):
    """
    Represents a link to an entity type.
    """

    source_name_linked_to: str
    """
    The source to which the link is pointing.
    """

    field_name_linked_to: str
    """
    The field of the destination entity through which the link is made.
    """

    type: Optional[LinkType] = None
    """
    Link cardinality.
    """

class LinkedFieldToSource(BaseModel):
    field_name: str
    """
    The name of the current entity type's field to which the link is made.
    """

    link: LinkToSource
    """
    The link.
    """

from .AbstractCRUDableEntityType import AbstractCRUDableEntityType
from .FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from .Fields import Fields
from .interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
Link.model_rebuild()