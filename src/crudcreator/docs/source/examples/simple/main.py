"""
Example of a very simple CRUD.
The SQL database data model contains a single entity ("books"),
and we wish to create only the 4 basic CRUD routes to interact with this entity.
"""


from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import os

from crudcreator.adaptator.sql.engine_wrapper.SQLEngineWrapper import SQLEngineAsyncWrapper, AbstractSQLEngineWrapper
from crudcreator.transaction.sql.SQLTransactionManager import SQLTransactionManager
from crudcreator.destination.rest.RESTCRUDBuilder import RESTCRUDBuilder
from crudcreator.builder.SetBuilder import SetBuilder, EntityDescriptor

loop = asyncio.new_event_loop()

def create_sql_engine() -> SQLEngineAsyncWrapper:
    """
    We create the object that will allow crudcreator to interact with the SQL database
    """
    return SQLEngineAsyncWrapper(#we use the asynchronous wrapper, as we use asynchronous sqlite drivers (but there's also a synchronous wrapper if required)
        engine=create_async_engine(#set the SQLAlchemy engine to use
            "sqlite+aiosqlite:///db.sqlite",#crudcreator works with all types of SQL databases (but we use SQLite for the examples).
            echo=False#set to True if you wish to print SQL queries sent to the database by crudcreator (useful for debugging)
        )
    )

async def create_list_crud_objects(sql_engine: AbstractSQLEngineWrapper):
    """
    We create the list of objects that will represent our entities (in this case, only a "book" entity).
    """
    return await SetBuilder().build(
        [
            EntityDescriptor(path=os.path.join("descriptors", "book.json"), export=True),
        ],
        {
            "engine_wrapper": sql_engine
        },
        {},
        {}
    )

async def create_api():
    """
    Creating the API with FastAPI
    """

    api = FastAPI()

    sql_engine = create_sql_engine()

    transaction_manager = SQLTransactionManager(
        engine_wrapper=sql_engine
    )

    #we create a REST interface, to which we add the entities we've created
    crud_builder = RESTCRUDBuilder(index_filter_override={})
    for crud_object in await create_list_crud_objects(sql_engine):#loop over all our created entities (here, only one "book" entity)
        crud_builder.build_read(crud_object, transaction_manager)#add a route for Read (GET)
        crud_builder.build_create(crud_object, transaction_manager)#add a route for Create (POST)
        crud_builder.build_delete(crud_object, transaction_manager)#we add a route for the Delete (DELETE)
        crud_builder.build_update(crud_object, transaction_manager)#add a route for the Update (PATCH)

    api.include_router(crud_builder.router)

    #You can add other manually written routes to the "api" object.

    return api

if __name__ == "__main__":
    """
    Start the server that will serve the API, using uvicorn (https://www.uvicorn.org/)
    """
    import uvicorn

    #we create the API in our asyncio loop
    api = loop.run_until_complete(create_api())

    #start the server
    loop.run_until_complete(
        uvicorn.Server(
            uvicorn.Config(
                app=api, 
                port=8000,
                loop=loop#we start the server in the same asyncio loop in which we created our routes
            )
        ).serve()
    )