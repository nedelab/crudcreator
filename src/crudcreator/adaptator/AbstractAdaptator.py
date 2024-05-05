
from ..source.AbstractCRUDableEntityTypeSource import AbstractCRUDableEntityTypeSource
from ..interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from pydantic import BaseModel

class AbstractAdaptatorParams(BaseModel):
    """
    Parameters for customizing the adaptator module.
    It's up to the AbstractAdaptatorParams implementations to build themselves as they should.
    """
    pass

class AbstractAdaptator(BaseModel):

    params: AbstractAdaptatorParams#TODO : not clean, useful only for giving type to AbstractDescriptor

    @classmethod
    async def build(
        cls,
        source_params: AbstractAdaptatorParams,
        interface: CRUDableEntityTypeInterface
    ) -> "AbstractCRUDableEntityTypeSource":
        """
        Method to call to instantiate the adaptator.

        :param source_params:
            See above.

        :param interface:
            See above.
        """
        raise NotImplementedError()