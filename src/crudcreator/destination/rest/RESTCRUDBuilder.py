
from .builder.build_bulk_update import _BulkUpdateRESTCRUDBuilder
from .builder.build_create import _CreateRESTCRUDBuilder
from .builder.build_delete import _DeleteRESTCRUDBuilder
from .builder.build_read import _ReadRESTCRUDBuilder
from .builder.build_update import _UpdateRESTCRUDBuilder
from .builder.build_update_or_create import _UpdateOrCreateRESTCRUDBuilder


class RESTCRUDBuilder(
    _BulkUpdateRESTCRUDBuilder, 
    _CreateRESTCRUDBuilder,
    _DeleteRESTCRUDBuilder,
    _ReadRESTCRUDBuilder,
    _UpdateRESTCRUDBuilder,
    _UpdateOrCreateRESTCRUDBuilder
):
    """
    Allows you to build a REST interface (FastAPI router) for several types of entities.
    """
    pass