from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db
import json
from .test_read import _read
from .test_delete import _delete
import pytest
from .test_create import _create
from datetime import datetime, timedelta

def _update(route: str, date_ids: dict, data: dict):
    with TestClient(app) as client:
        ret = client.patch(route, params=date_ids, json=data)
        assert ret.status_code == 200
        read_response = ret.json()
        print(read_response)
        assert read_response is None
        return read_response
    
#entity1

@pytest.mark.asyncio
async def test_update_entity_1_one_field():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 0
    create_response = _update(
        "/entity1", {
                "field_text_primary_not_null_no_default": "pk2"
            }, {
                "field_text_primary_not_null_no_default": "pk3"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["field_int"] == 2
    assert entity["field_text_primary_not_null_no_default"] == "pk3"
    assert entity["field_text_not_null_default"] == "test2"
    assert entity["field_text_default"] == "other_test_2"
    assert entity["field_text_no_default"] == "no_default_2"
    assert entity["field_text_overwritten_default"] == "overwritten_default_2"
    assert entity["field_bool_converted"] == False
    assert entity["field_text_not_writable"] == "not_writable_2"
    assert entity["field_text_not_writable_no_default"] == "not_writable_no_default_2"


@pytest.mark.asyncio
async def test_update_entity_1_all_field():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 0
    create_response = _update(
        "/entity1", {
                "field_text_primary_not_null_no_default": "pk2"
            }, {
                "field_int": 3,
                "field_text_primary_not_null_no_default": "pk3",
                "field_text_not_null_default": "test3",
                "field_text_default": "other_test_3",
                "field_text_no_default": "no_default_3",
                "field_text_overwritten_default": "overwritten_default_3",
                "field_bool_converted": True,
                "field_text_updatable_not_creatable": "test"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["field_int"] == 3
    assert entity["field_text_primary_not_null_no_default"] == "pk3"
    assert entity["field_text_not_null_default"] == "test3"
    assert entity["field_text_default"] == "other_test_3"
    assert entity["field_text_no_default"] == "no_default_3"
    assert entity["field_text_overwritten_default"] == "overwritten_default_3"
    assert entity["field_bool_converted"] == True
    assert entity["field_text_updatable_not_creatable"] == "test"
    #not updatable
    assert entity["field_text_not_writable"] == "not_writable_2"
    assert entity["field_text_not_writable_no_default"] == "not_writable_no_default_2"
    assert entity["field_text_creatable_not_updatable"] == "creatable_not_updatable_no_default_2"


@pytest.mark.asyncio
async def test_update_entity_1_not_writable_field():
    """
    On vérifie que les champs "not wirtable" ne change pas quand on essaye de les modifier
    """
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["field_text_not_writable"] == "not_writable_2"
    assert entity["field_text_not_writable_no_default"] == "not_writable_no_default_2"
    create_response = _update(
        "/entity1", {
                "field_text_primary_not_null_no_default": "pk2"
            }, {
                "field_text_not_writable": "test",
                "field_text_not_writable_no_default": "test",
                "field_text_creatable_not_updatable": "test"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["field_text_not_writable"] == "not_writable_2"
    assert entity["field_text_not_writable_no_default"] == "not_writable_no_default_2"
    assert entity["field_text_creatable_not_updatable"] == "creatable_not_updatable_no_default_2"


@pytest.mark.asyncio
async def test_update_entity_1_confilct():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.patch("/entity1", 
                params={
                    "field_text_primary_not_null_no_default": "pk2"
                },
            json={
                "field_int": 3,
                "field_text_primary_not_null_no_default": "pk1",
                "field_text_no_default": "no_default_3"
                })
    assert ret.status_code == 409


@pytest.mark.asyncio
async def test_update_entity_1_not_exists():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.patch("/entity1", 
                params={
                    "field_text_primary_not_null_no_default": "does_not_exist"
                },
            json={
                "field_int": 3,
                "field_text_primary_not_null_no_default": "pk3",
                "field_text_no_default": "no_default_3"
                })
    assert ret.status_code == 404


@pytest.mark.asyncio
async def test_update_entity_9_no_confilct():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.patch("/entity9", 
                params={
                    "field_not_pk_becomes_pk": 1,
                    "field_not_pk_becomes_pk_default": 1
                },
            json={
                "field_not_pk_becomes_pk": 10
                })
    assert ret.status_code == 200


@pytest.mark.asyncio
async def test_update_entity_9_confilct():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.patch("/entity9", 
                params={
                    "field_not_pk_becomes_pk": 1,
                    "field_not_pk_becomes_pk_default": 1
                },
            json={
                "field_not_pk_becomes_pk": 2,
                "field_not_pk_becomes_pk_default": 2
                })
    assert ret.status_code == 409

@pytest.mark.asyncio
async def test_update_entity_20_one_field():
    await reinit_db()
    read_reponse = _read("/entity20", {
        "column_1": "1"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity20", {
        "column_1": "5"
    })
    assert len(read_reponse) == 0
    create_response = _update(
        "/entity20", {
                "column_2": "1"#is ignored. TODO : must raise error ?
            }, {
                "column_1": "5"
            }
    )
    read_reponse = _read("/entity20", {
        "column_1": "1"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity20", {
        "column_1": "5"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["column_2"] == "1"

@pytest.mark.asyncio
async def test_update_entity_20_not_in_id_firewall():
    await reinit_db()
    read_reponse = _read("/entity20", {
        "column_1": "1"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity20", {
        "column_1": "5"
    })
    assert len(read_reponse) == 0
    create_response = _update(
        "/entity20", {
                "column_1": "1"
            }, {
                "column_2": "5"
            }
    )
    read_reponse = _read("/entity20", {
        "column_2": "1"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity20", {
        "column_2": "5"
    })
    assert len(read_reponse) == 4
    assert not all([entity["column_1"] == "1" for entity in read_reponse])

@pytest.mark.asyncio
async def test_update_entity_24():
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

    create_response = _update(
        "/entity24", {
                "column_2": "1"
            }, {
                "column_1": "5"
            }
    )
    read_reponse_1 = _read("/entity24", {
        "column_2": "1"
    })
    assert len(read_reponse_1) == 1
    entity = read_reponse_1[0]
    assert datetime.fromisoformat(entity["creation_date"]) == creation_date
    last_update_date = datetime.fromisoformat(entity["last_update_date"])
    assert last_update_date > datetime.now()-timedelta(seconds=10)
    assert last_update_date < datetime.now()+timedelta(seconds=10)

    create_response = _update(
        "/entity24", {
                "column_2": "1"
            }, {
                "column_1": "5"
            }
    )
    read_reponse_1 = _read("/entity24", {
        "column_2": "1"
    })
    assert len(read_reponse_1) == 1
    entity = read_reponse_1[0]
    assert datetime.fromisoformat(entity["creation_date"]) == creation_date
    assert last_update_date != datetime.fromisoformat(entity["last_update_date"])
    last_update_date = datetime.fromisoformat(entity["last_update_date"])
    assert last_update_date > datetime.now()-timedelta(seconds=10)
    assert last_update_date < datetime.now()+timedelta(seconds=10)

@pytest.mark.asyncio
async def test_update_entity_25_no_password():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    with TestClient(app) as client:
        ret = client.patch("/entity25", params={"username": "user2", "field_id": 1}, json={"field_id": 4})
    assert ret.status_code == 401
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_update_entity_25_bad_password():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    with TestClient(app) as client:
        ret = client.patch("/entity25", params={"username": "user2", "field_id": 1}, json={"field_id": 4}, auth=("user1", "wrong_password"))
    assert ret.status_code == 401
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_update_entity_25_bad_user():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    with TestClient(app) as client:
        ret = client.patch("/entity25", params={"username": "user2", "field_id": 1}, json={"field_id": 4}, auth=("does_not_exist", "test_password"))
    assert ret.status_code == 404
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_update_entity_25_good_password():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    with TestClient(app) as client:
        ret = client.patch("/entity25", params={"username": "user2", "field_id": 1}, json={"field_id": 4}, auth=("user1", "test_password"))
    assert ret.status_code == 200
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    ids = [4, 10]
    assert read_reponse[0]["field_id"] in ids
    assert read_reponse[1]["field_id"] in ids
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_update_entity_6_after_soft_delete():
    """
    On crée, on supprime, et on recrée, et on update.
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

    create_response = _create(
        "/entity6", 
        {
            "field_id": 5
        }
    )
    read_reponse_1 = _read("/entity6", {
        "field_id": 5
    })
    assert len(read_reponse_1) == 1
    read_reponse_1 = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse_1) == 0
    
    with TestClient(app) as client:
        ret = client.patch("/entity6", 
            params={"field_id": 5}, 
            json={"field_id": 1}
        )
        assert ret.status_code == 200
    read_reponse_1 = _read("/entity6", {
        "field_id": 5
    })
    assert len(read_reponse_1) == 0
    read_reponse_1 = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse_1) == 1
    
@pytest.mark.asyncio
async def test_update_entity_27():
    await reinit_db()

    read_reponse = _read("/entity27", {
        "field_1": 1
    })
    assert len(read_reponse) == 2

    read_reponse = _read("/entity27", {})
    assert len(read_reponse) == 5

    read_reponse = _read("/entity27", {
        "field_2": 6
    })
    assert len(read_reponse) == 0

    create_response = _update(
        "/entity27", {}, {
                "field_2": 6
            }
    )

    read_reponse = _read("/entity27", {
        "field_1": 1
    })
    assert len(read_reponse) == 2

    read_reponse = _read("/entity27", {})
    assert len(read_reponse) == 5

    read_reponse = _read("/entity27", {
        "field_2": 6
    })
    assert len(read_reponse) == 2

#TODO : test update cascade
