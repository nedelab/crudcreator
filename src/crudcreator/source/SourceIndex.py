from .AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from .source import SQLSource
from ..adaptator import SimpleSQLAdaptator

list_source: list[AbstractCRUDableEntityTypeSource] = [
    SQLSource
]

source_index: dict[str, AbstractCRUDableEntityTypeSource] = {
    source.__name__:source for source in list_source
}

