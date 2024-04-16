from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db
import json
from .test_read import _read
from .test_delete import _delete
import pytest
from datetime import datetime, timedelta

def _create(route: str, data: dict):
    with TestClient(app) as client:
        ret = client.post(route, json=data)
        assert ret.status_code == 200
        read_response = ret.json()
        print(read_response)
        assert read_response is None
        return read_response
    
#entity1
@pytest.mark.asyncio
async def test_create_entity_1_all_specified():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity1", {
            "field_to_join": 1,
            "field_int": 3,
            "field_text_primary_not_null_no_default": "pk3",
            "field_text_not_null_default": "test3",
            "field_text_default": "other_test_3",
            "field_text_no_default": "no_default_3",
            "field_text_overwritten_default": "overwritten_default_3",
            "field_bool_converted": True,
            "field_text_creatable_not_updatable": "creatable_not_updatable_3",
            "field_text_updatable_not_creatable": "test"
        }
    )
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["field_test"] == "test_join"
    assert entity["field_int"] == 3
    assert entity["field_text_primary_not_null_no_default"] == "pk3"
    assert entity["field_text_not_null_default"] == "test3"
    assert entity["field_text_default"] == "other_test_3"
    assert entity["field_text_no_default"] == "no_default_3"
    assert entity["field_text_overwritten_default"] == "overwritten_default_3"
    assert entity["field_bool_converted"] == True
    assert entity["field_text_creatable_not_updatable"] == "creatable_not_updatable_3"
    #les colonnes non créables
    assert entity["field_text_not_writable"] == "default_value_not_writable"
    assert entity["field_text_not_writable_no_default"] is None
    assert entity["field_text_updatable_not_creatable"] is None

@pytest.mark.asyncio
async def test_create_entity_1_default():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity1", {
            "field_to_join": 1,
            "field_int": 3,
            "field_text_primary_not_null_no_default": "pk3",
            "field_text_no_default": "no_default_3"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["field_test"] == "test_join"
    assert entity["field_int"] == 3
    assert entity["field_text_primary_not_null_no_default"] == "pk3"
    assert entity["field_text_not_null_default"] == "default_value_not_null"
    assert entity["field_text_default"] == "default_value"
    assert entity["field_text_no_default"] == "no_default_3"
    assert entity["field_text_overwritten_default"] == "overwritten_default"
    assert entity["field_bool_converted"] == True#un défaut converti sur cette colonne
    #les colonnes non écrivable
    assert entity["field_text_not_writable"] == "default_value_not_writable"
    assert entity["field_text_not_writable_no_default"] is None
    assert entity["field_text_updatable_not_creatable"] is None

@pytest.mark.asyncio
async def test_create_entity_1_not_null_no_default_no_present():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity1", json={
            "field_to_join": 1,
            "field_int": 3,
            "field_text_no_default": "no_default_3"
            })
    assert ret.status_code == 422

@pytest.mark.asyncio
async def test_create_entity_1_conflict():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity1", json={
            "field_to_join": 1,
            "field_int": 3,
            "field_text_primary_not_null_no_default": "pk2",
            "field_text_no_default": "no_default_3"
            })
    assert ret.status_code == 409

@pytest.mark.asyncio
async def test_create_entity_2_unicity_not_enforced_in_base():
    await reinit_db()
    print(app)
    with TestClient(app) as client:
        ret = client.post("/entity2", json={
            "field_pk_becomes_not_pk": 3,
            "field_not_pk_becomes_pk": 3
            })
        assert ret.status_code == 200
        ret = client.post("/entity2", json={
            "field_pk_becomes_not_pk": 4,
            "field_not_pk_becomes_pk": 3
            })
        assert ret.status_code == 409
   
@pytest.mark.asyncio     
async def test_create_entity_7():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity7", json={
            "column_id": 1,
            "sort1": 3,
            "sort2": 3
            })

@pytest.mark.asyncio
async def test_create_entity_8_several_times_autoincrement():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity8", json={
            "field_2": "test"
            })
        assert ret.status_code == 200
        ret = client.post("/entity8", json={
            "field_2": "test"
            })
        assert ret.status_code == 200
        ret = client.post("/entity8", json={
            "field_2": "test"
            })
        assert ret.status_code == 200


@pytest.mark.asyncio
async def test_create_entity_9_unicity_not_enforced_in_base_1():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 3,
            "field_not_pk_becomes_pk": 3,
            "field_not_pk_becomes_pk_default": 3
            })
        assert ret.status_code == 200
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 4,
            "field_not_pk_becomes_pk": 3,
            "field_not_pk_becomes_pk_default": 4
            })
        assert ret.status_code == 200
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 5,
            "field_not_pk_becomes_pk": 4,
            "field_not_pk_becomes_pk_default": 3
            })
        assert ret.status_code == 200
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 6,
            "field_not_pk_becomes_pk": 3,
            "field_not_pk_becomes_pk_default": 3
            })
        assert ret.status_code == 409

@pytest.mark.asyncio
async def test_create_entity_9_unicity_not_enforced_in_base_2():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 3,
            "field_not_pk_becomes_pk": 3,
            })
        assert ret.status_code == 200
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 4,
            "field_not_pk_becomes_pk": 4,
            })
        assert ret.status_code == 200
        ret = client.post("/entity9", json={
            "field_pk_becomes_not_pk": 5,
            "field_not_pk_becomes_pk": 4,
            })
        assert ret.status_code == 409

@pytest.mark.asyncio
async def test_create_entity_10_unicity_not_enforced_in_base_1():
    """
    Jamais de pb d'unicité, car il y a un id en autoincrement
    """
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post("/entity10", json={
            "field_pk_becomes_not_pk": 3,
            "field_not_pk_becomes_pk": 3,
            "field_not_pk_becomes_pk_default": 3
        })
        assert ret.status_code == 200
        ret = client.post("/entity10", json={
            "field_pk_becomes_not_pk": 4,
            "field_not_pk_becomes_pk": 3,
            "field_not_pk_becomes_pk_default": 4
        })
        assert ret.status_code == 200
        ret = client.post("/entity10", json={
            "field_pk_becomes_not_pk": 5,
            "field_not_pk_becomes_pk": 4,
            "field_not_pk_becomes_pk_default": 3
        })
        assert ret.status_code == 200
        ret = client.post("/entity10", json={
            "field_pk_becomes_not_pk": 6,
            "field_not_pk_becomes_pk": 3,
            "field_not_pk_becomes_pk_default": 3
        })
        assert ret.status_code == 200

@pytest.mark.asyncio
async def test_create_entity_1_str_too_large():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.post(
            "/entity1", 
            json={
                "field_to_join": 1,
                "field_int": 3,
                "field_text_primary_not_null_no_default": "A"*99,
                "field_text_not_null_default": "test3",
                "field_text_default": "other_test_3",
                "field_text_no_default": "no_default_3",
                "field_text_overwritten_default": "overwritten_default_3",
                "field_bool_converted": True
            })
        print(ret.json())
        assert ret.status_code == 200
        ret = client.post(
            "/entity1", 
            json={
                "field_to_join": 1,
                "field_int": 4,
                "field_text_primary_not_null_no_default": "A"*105,
                "field_text_not_null_default": "test3",
                "field_text_default": "other_test_3",
                "field_text_no_default": "no_default_3",
                "field_text_overwritten_default": "overwritten_default_3",
                "field_bool_converted": True
            })
        print(ret.json())
        assert ret.status_code == 422


#entity18
@pytest.mark.asyncio
async def test_create_entity_18():
    #on teste la création en cascade
    await reinit_db()
    read_reponse = _read("/entity18", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 3
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity18", {
            "field_to_join": 3
        }
    )
    read_reponse = _read("/entity18", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 1
    #au cas où
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 3
    })
    assert len(read_reponse) == 1

@pytest.mark.asyncio
async def test_create_entity_20():
    await reinit_db()
    read_reponse = _read("/entity20", {
        "column_1": "5"
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity20", {
            "column_1": "5",
            "column_2": "5",
        }
    )
    read_reponse = _read("/entity20", {
        "column_1": "5"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["column_1"] == "5"
    assert entity["column_2"] == "5"
    assert entity["group"] == []

@pytest.mark.asyncio
async def test_create_entity_21():
    #default est un Field avec default factory
    await reinit_db()
    read_reponse = _read("/entity21", {
        "field_2": 5
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity21", {
            "field_2": 5,
        }
    )
    read_reponse_1 = _read("/entity21", {
        "field_2": 5
    })
    assert len(read_reponse_1) == 1
    entity = read_reponse_1[0]
    assert type(entity["field_1"]) == int
    assert entity["field_2"] == 5

    read_reponse = _read("/entity21", {
        "field_2": 6
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity21", {
            "field_2": 6,
        }
    )
    read_reponse_2 = _read("/entity21", {
        "field_2": 6
    })
    assert len(read_reponse_2) == 1
    entity = read_reponse_2[0]
    assert type(entity["field_1"]) == int
    assert entity["field_2"] == 6

    assert read_reponse_2[0]["field_1"] != read_reponse_1[0]["field_1"] 

    
@pytest.mark.asyncio
async def test_create_entity_21_2():
    #default avec AddDefault
    await reinit_db()
    read_reponse = _read("/entity21", {
        "field_2": 10
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity21", {}
    )
    read_reponse_1 = _read("/entity21", {
        "field_2": 10
    })
    assert len(read_reponse_1) == 1
    entity = read_reponse_1[0]
    assert type(entity["field_1"]) == int
    assert entity["field_2"] == 10

@pytest.mark.asyncio
async def test_create_entity_24():
    #add writer value
    await reinit_db()
    read_reponse = _read("/entity24", {
        "column_2": "1"
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity24", {
           "column_1": "1",
           "column_2": "1" 
        }
    )
    read_reponse_1 = _read("/entity24", {
        "column_2": "1"
    })
    assert len(read_reponse_1) == 1
    entity = read_reponse_1[0]
    creation_date = datetime.fromisoformat(entity["creation_date"])
    assert creation_date > datetime.now()-timedelta(seconds=10)
    assert creation_date < datetime.now()+timedelta(seconds=10)
    assert entity["last_update_date"] is None

@pytest.mark.asyncio
async def test_create_entity_6_after_soft_delete():
    """
    On crée, on supprime, et on recrée.
    Ne doit pas y avoir d'erreur d'unicité non respectée (même si la ligne existe toujours dans le sql après le delete).
    """
    await reinit_db()
    read_reponse = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse) == 1
    _delete(
        "/entity6", {
            "field_id": 1
        }
    )
    read_reponse = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse) == 0

    read_reponse = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse) == 0
    create_response = _create(
        "/entity6", 
        {
            "field_id": 1
        }
    )
    read_reponse_1 = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse_1) == 1