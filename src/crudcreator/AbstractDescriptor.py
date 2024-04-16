from pydantic import BaseModel, validator
from typing import Any, TypeVar, Generic, Type
from .AbstractCRUDableEntityType import AbstractCRUDableEntityType

T = TypeVar("T")
U = TypeVar("U")
class AbstractDescriptor(BaseModel, Generic[T, U]):
    """
    Describes a module, without having built it.
    Is an intermediate class used by CRUD constructors to build entity types.
    Library users should never have to use this class directly.
    """
    
    name: str
    """
    Name of the module to be built.
    """

    params: dict
    """
    Parameters of the module to be built.
    """

    subs_index: dict[str, Any]
    """
    Index of Python objects associated with variables in the descriptor.
    """

    addons: dict[str, Type[AbstractCRUDableEntityType]]
    """
    Index of personal modules implemented by the crudcreator user.
    """

    """@validator("name")
    def name_exists(cls, name):
        if name not in cls.get_index():
            raise ValueError(f"{name} n'existe pas")
        return name"""
    
    def get_index(self) -> dict[str, Any]:
        """
        To be overloaded. Must return the index of modules pre-implemented by the library.
        """
        raise NotImplementedError()
    
    def build(self) -> AbstractCRUDableEntityType:
        """
        To be overloaded. Builds the entity type associated with this descriptor.
        """
        raise NotImplementedError()
    
    def get_class(self) -> T:
        """
        Returns the class associated with the descriptor.
        Fetches the class from the index of modules pre-implemented by crudcreator.
        Otherwise, search in addons.
        """
        index = self.get_index()
        if self.name in index:
            return self.get_index()[self.name]
        else:
            return self.addons[self.name]
    
    def get_params_class(self) -> Type[BaseModel]:
        """
        Returns the pydantic model of the module parameters associated with the descriptor.
        """
        return self.get_class().model_fields["params"].annotation
    
    def get_params(self) -> U:
        """
        Builds the parameters associated with the descriptor, after substituting variables with their Python object.
        """
        return self.get_params_class()(**self._get_params_dict_subst(self.params))
    
    def _get_params_dict_subst(self, params: Any) -> Any:
        """
        Replaces "$var$" with subs_index["var"].
        Allows to have parameters that are indescribable in json, and that must be created
        directly in the code at construction time.
        """
        if type(params) == str:
            if (
                len(params) > 2 and
                params[0] == "$" and
                params[-1] == "$" and
                params[1:-1] in self.subs_index 
            ):
                return self.subs_index[params[1:-1]]
            else:
                return params
        elif type(params) == dict:
            return {k:self._get_params_dict_subst(v) for k,v in params.items()}
        elif type(params) == list:
            return [self._get_params_dict_subst(e) for e in params]
        else:
            return params
                
        
