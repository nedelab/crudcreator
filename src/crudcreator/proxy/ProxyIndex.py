from .AbstractCRUDableEntityTypeProxy import AbstractCRUDableEntityTypeProxy
from .proxy import AddIdValue, UpdateFirewall, CreateFirewall, AddWriteValue, GatherFields, AddDefault, GroupBy, CreateLink, AddFilter, AddOptions, FilterFirewall, ReadFirewall, Rename, SoftDelete, RecastType, CascadeDelete, CascadeCreateAndUpdate, AddSort, ReadDistinct, ReadDistinctFirewall
from ..adaptator.sql.proxy import SQLPagination, SQLCreateLink, SQLFilter, SQLReadFromLink, SQLRequestConstructor, SQLRequestExecutor, SQLSort

list_proxy: list[AbstractCRUDableEntityTypeProxy] = [
    AddFilter,
    AddOptions,
    FilterFirewall,
    ReadFirewall,
    Rename,
    SoftDelete,
    SQLFilter, 
    SQLCreateLink,
    SQLReadFromLink, 
    SQLRequestConstructor, 
    SQLRequestExecutor, 
    SQLSort,
    RecastType,
    CreateLink,
    CascadeDelete, 
    CascadeCreateAndUpdate,
    GroupBy,
    AddDefault,
    GatherFields,
    AddWriteValue,
    UpdateFirewall,
    CreateFirewall,
    AddIdValue,
    SQLPagination,
    AddSort,
    ReadDistinct,
    ReadDistinctFirewall
]

proxy_index: dict[str, AbstractCRUDableEntityTypeProxy] = {
    proxy.__name__:proxy for proxy in list_proxy
}

    