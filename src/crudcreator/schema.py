
from pydantic import BaseModel
from .transaction.AbstractTransaction import AbstractTransaction
from .transaction.AbstractTransactionManager import AbstractTransactionManager
from .Filter import FilterInstance
from typing import Any

class ReadParams(BaseModel):
    """
    The parameters expected by the *read* method of the entity types.
    Contains the information required for a CRUD read request.
    """

    transaction: AbstractTransaction
    """
    The open transaction.
    """

    list_filter_instance: list[FilterInstance]
    """
    Reading filters.
    """

    list_read_field: list[str]
    """
    Fields to be read.
    """

    dict_read_options: dict[str, Any]
    """
    Reading options. Will be read by proxies to potentially modify their behavior.
    """

class CreateParams(BaseModel):
    """
    The parameters expected by the *create* method of the entity types.
    Contains the information required for a CRUD create request.
    """

    transaction: AbstractTransaction

    dict_creator_value: dict[str, Any]
    """
    Field values for the new entity to be created.
    """

    dict_creator_options: dict[str, Any]
    """
    Creation options. Will be read by proxies to potentially modify their behavior.
    """

class UpdateParams(BaseModel):
    """
    The parameters expected by the *update* method of the entity types.
    Contains the information required for a CRUD update request.
    """

    transaction: AbstractTransaction

    dict_ids: dict[str, Any]
    """
    The value of the ids used to identify the entity to be modified.
    """

    dict_updator_value: dict[str, Any]
    """
    The new value of the fields to be updated.
    """

    dict_updator_options: dict[str, Any]
    """
    Modification options. Will be read by proxies to potentially modify their behavior.
    """

class DeleteParams(BaseModel):
    """
    Parameters expected by the *delete* method of entity types.
    Contains the information required for a CRUD delete request.
    """

    transaction: AbstractTransaction

    dict_deletor_value: dict[str, Any]
    """
    The value of the ids used to identify the entity to be modified.
    """

    dict_deletor_options: dict[str, Any]
    """
    Deletion options. Will be read by proxies to potentially modify their behavior.
    """

class UpdateOrCreateParams(BaseModel):
    """
    Parameters expected by the *update_or_create* method for entities.
    """

    transaction_manager: AbstractTransactionManager

    dict_ids: dict[str, Any]
    """
    The value of the ids used to identify the entity to be modified.
    """

    dict_update_or_create_value: dict[str, Any]
    """
    Field values for the new entity to be created (or updated).
    """

    dict_update_or_create_options: dict[str, Any]
    """
    Creation or modification options. Will be read by proxies to potentially modify their behavior.
    """
