import sqlite3
import os
from typing import Any
from test.engine import engine_wrapper
from test.settings import settings, DatabaseType
from sqlalchemy import text
from src.crudcreator.proxy.ProxyDescriptor import ProxyDescriptor
from src.crudcreator.proxy.proxy  import AddFilter, AddFilterParams
from src.crudcreator.builder.SetBuilder import SetBuilder, EntityDescriptor
from src.crudcreator.interface.CRUDableEntityTypeInterface import CRUDableEntityTypeInterface
from src.crudcreator.adaptator.sql.SQLColumnInspector import SQLColumnInspector
from src.crudcreator.source.source.SQLSource import SQLSource
from test.engine import engine_wrapper
import os
from src.crudcreator.proxy.proxy.type.SpecialType import SpecialType
from test.addons import TestOption

from fastapi import Header, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import HTTPException
import random
from pydantic import Field
from datetime import datetime

async def reinit_db():
    list_filename = [
        "reinit_1.sql", 
        "reinit_2.sql", 
        "reinit_3.sql", 
        "reinit_5.sql", 
        "reinit_6.sql", 
        "reinit_7.sql",
        "reinit_9.sql",
        "reinit_11.sql",
        "reinit_12.sql",
        "reinit_13.sql",
        "reinit_14.sql",
        "reinit_15.sql",
        "reinit_user.sql",
        "reinit_16.sql",
        "reinit_17.sql",
        "reinit_18.sql",
        "reinit_19.sql",
        "reinit_20.sql",
        "reinit_many.sql",
        "reinit_21.sql",
        "reinit_22.sql",
        "reinit_23.sql",
        "reinit_24.sql",
        "reinit_25.sql",
        "reinit_26.sql",
        "reinit_27.sql",
    ]
    if settings.database_type == DatabaseType.postgres or settings.database_type == DatabaseType.async_postgres:
        list_filename.append("reinit_4_postgres.sql")
        list_filename.append("reinit_8_postgres.sql")
        list_filename.append("reinit_10_postgres.sql")
    elif settings.database_type == DatabaseType.sqlite:
        list_filename.append("reinit_4_sqlite.sql")
        list_filename.append("reinit_8_sqlite.sql")
        list_filename.append("reinit_10_sqlite.sql")
    async with engine_wrapper.begin() as conn:
        for filename in list_filename:
            with open(os.path.join(os.path.dirname(__file__), "sql", filename)) as f:
                for sql_req in f.read().split(";"):
                    if len(sql_req.strip()) > 0:
                        await conn.execute(text(sql_req))
                await conn.execute(text("COMMIT;"))

def check_dict_key_value(d: dict, key: Any, value_value: Any):
    assert key in d
    assert d[key] == value_value

def check_dict_key_type(d: dict, key: Any, value_type: Any):
    assert key in d
    assert type(d[key]) == value_type


def get_username(creds: HTTPBasicCredentials = Depends(HTTPBasic())):
    if creds.password == "test_password":
        return creds.username
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
def oui_non_to_bool(v: str):
    if v == "oui":
        return True
    elif v == "non":
        return False
    elif v == None:
        return None
    else:
        raise NotImplementedError()
    
def bool_to_oui_non(v: bool):
    if v == True:
        return "oui"
    elif v == False:
        return "non"
    elif v == None:
        return None
    else:
        raise NotImplementedError()

def random_int():
    return random.randint(0, 1000000000000)    
        
oui_non_type = SpecialType(
        destination_type=bool,
        destination_to_source=bool_to_oui_non,
        source_to_destination=oui_non_to_bool
    )

async def create_list_crud_object():

    return await SetBuilder().build(
        [
            EntityDescriptor(path=os.path.join("test", "descriptor", "user.json"), export=False),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entitymany.json"), export=False),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity3.json"), export=False),#une première passe pour les référence
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity1.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity2.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity3.json"), export=True),#puis on exporte
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity4.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity6.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity7.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity7_bis.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity8.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity9.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity10.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity11.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity12.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity13.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity14.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity15.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity16.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity17.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity18.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity19.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity20.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity21.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity22.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity23.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity24.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity25.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity26.json"), export=True),
            EntityDescriptor(path=os.path.join("test", "descriptor", "entity27.json"), export=True),
        ],
        {
            "engine_wrapper": engine_wrapper,
            "oui_non_type": oui_non_type,
            "get_username": Depends(get_username),
            "table1_var": "table1",
            "random_int": Field(default_factory=random_int),
            "now": datetime.now
        },
        {},
        {
            "TestOption": TestOption
        }
    )