from typing import Any
from pydantic import BaseModel, create_model
from typing import Optional
from ...Sentinel import Sentinel
from ..AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from...AbstractCRUDableEntityType import AbstractCRUDableEntityType
from ...FieldOfCRUDableEntityType import FieldOfCRUDableEntityType
from ...Fields import Fields
from ...Filter import FilterInstance, FilterationEnum
from ...interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from ..AbstractProxyParams import AbstractProxyParams
from ...transaction.AbstractTransaction import AbstractTransaction
from ...schema import ReadParams, CreateParams, UpdateParams, DeleteParams
import functools

class FieldValueIfDeleted(BaseModel):

    field_name: str
    """
    The field whose value determines whether an entity is deleted or not.
    """

    value_if_deleted: Any
    """
    The value of the field indicating whether the entity is deleted.
    TODO: allow to enter a function (datetime.now for example).
    """

    keep_visible: bool
    """
    Indicates whether the field can still be read, or whether it is completely invisible to the CRUD user.
    """

class SoftDeleteParams(AbstractProxyParams):
    """
    SoftDelete proxy settings.
    """

    list_field_value_if_deleted : list[FieldValueIfDeleted]
    """
    List of fields/values that indicate that the entity is deleted.
    This is an "OR" for reading: if only one of the fields has the value "value_if_deleted", then the field is considered deleted.
    On the other hand, "delete" will set all the fields in the list to the correct value.
    """
    
    @functools.cached_property
    def value_if_deleted_index(self) -> dict[str, FieldValueIfDeleted]:
        """
        Index field_name->FieldValueIfDeleted automatically created from list_field_value_if_deleted.
        """
        return {t.field_name:t for t in self.list_field_value_if_deleted}
    
class SoftDelete(AbstractCRUDableEntityTypeProxy):
    """
    Transforms the delete into a "soft delete". The delete thus becomes an update on fields that will indicate
    whether or not the entity should be considered as deleted.

    Example of descriptor, which, when read, only returns entities where is_active!=false and is_deleted!=true.
    The "is_active" value of each entity will remain visible on reading (but not that of the "is_deleted" field,
    which therefore does not exist in the eyes of the CRUD user).

    .. highlight:: json
    .. code-block:: json

        {
            "name": "SoftDelete",
            "params": {
                "list_field_value_if_deleted": [
                    {
                        "field_name": "is_active",
                        "value_if_deleted": false,
                        "keep_visible": true
                    },
                    {
                        "field_name": "is_deleted",
                        "value_if_deleted": true,
                        "keep_visible": false
                    }
                ]
            }
        }
    """
    #Requires an AddValue proxy to add the values of fields associated with the delete on creation.

    params: SoftDeleteParams
    """
    SoftDelete proxy settings.
    """

    @staticmethod
    def _get_updated_interface(base_interface: CRUDableEntityTypeInterface, params: SoftDeleteParams):
        base_interface.fields = Fields.build([
            field 
            for field in base_interface.fields.list_field 
            if field.name not in params.value_if_deleted_index or params.value_if_deleted_index[field.name].keep_visible
        ])
        return base_interface
        #TODO : assert field.list_allowed_filter_type is None or FilterationEnum.different_of in [allowed_filter_type.filtration_type for allowed_filter_type in field.list_allowed_filter_type]

    async def read(self, params: ReadParams) -> list[dict[str, Any]]:
        """
        We only read entities that have not been soft deleted.
        """
        return await self.base.read(
            ReadParams(
                transaction=params.transaction,
                list_filter_instance=params.list_filter_instance+
                [
                    FilterInstance(
                        field_name=field_name,
                        filter_value=v.value_if_deleted,
                        filtration_type=FilterationEnum.different_of
                    )
                    for field_name, v in self.params.value_if_deleted_index.items()
                ],
                list_read_field=params.list_read_field,
                dict_read_options=params.dict_read_options
            )
        )
    
    async def delete(self, params: DeleteParams):
        """
        The delete becomes an update of the fields indicating deletion.
        """
        return await self.base.update(
            UpdateParams(
                transaction=params.transaction,
                dict_ids=params.dict_deletor_value,
                dict_updator_value={
                    field_name:v.value_if_deleted
                    for field_name, v in self.params.value_if_deleted_index.items()
                },
                dict_updator_options={}
            )
        )
    
    