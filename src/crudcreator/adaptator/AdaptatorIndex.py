from .AbstractAdaptator import AbstractAdaptator
from ..adaptator import SimpleSQLAdaptator

list_adaptator: list[AbstractAdaptator] = [
    SimpleSQLAdaptator
]

adaptator_index: dict[str, AbstractAdaptator] = {
    adaptator.__name__:adaptator for adaptator in list_adaptator
}

    