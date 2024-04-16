from fastapi import FastAPI, Depends
from src.crudcreator.destination.rest.RESTCRUDBuilder import RESTCRUDBuilder
import os
import json
from test.utils import create_list_crud_object, get_username
from src.crudcreator.transaction.sql.SQLTransactionManager import SQLTransactionManager
from test.engine import engine_wrapper
import asyncio
from test.loop import loop

async def create_app():
    app = FastAPI()

    transaction_manager = SQLTransactionManager(engine_wrapper=engine_wrapper)

    crud_builder = RESTCRUDBuilder(index_filter_override={})
    for crud_object in await create_list_crud_object():
        if crud_object.interface.name in ["entity15", "entity25"]:
            crud_builder.build_read(crud_object, transaction_manager, filter_from_dependencies={"username": Depends(get_username)})
        else:
            crud_builder.build_read(crud_object, transaction_manager)
        crud_builder.build_create(crud_object, transaction_manager)
        if crud_object.interface.name in ["entity25"]:
            crud_builder.build_update(crud_object, transaction_manager, ids_from_dependencies={"username": Depends(get_username)})
            crud_builder.build_update_or_create(crud_object, transaction_manager, ids_from_dependencies={"username": Depends(get_username)}, values_from_dependencies={"username": Depends(get_username)})
            crud_builder.build_delete(crud_object, transaction_manager, ids_from_dependencies={"username": Depends(get_username)})
        else:
            crud_builder.build_update(crud_object, transaction_manager)
            crud_builder.build_update_or_create(crud_object, transaction_manager)
            crud_builder.build_delete(crud_object, transaction_manager)
        if crud_object.interface.name in ["entity1", "entity24"]:
            crud_builder.build_bulk_update(crud_object, transaction_manager)
        elif crud_object.interface.name in ["entity25"]:
            crud_builder.build_bulk_update(crud_object, transaction_manager, ids_from_dependencies={"username": Depends(get_username)})

    app.include_router(crud_builder.router)

    return app

app = loop.run_until_complete(create_app())