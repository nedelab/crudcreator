from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db
import json
from .test_read import _read
import pytest

def _update_or_create(route: str, date_ids: dict, data: dict, **kwargs):
    with TestClient(app) as client:
        ret = client.put(route, params=date_ids, json=data, **kwargs)
        assert ret.status_code == 200
        read_response = ret.json()
        print(read_response)
        assert read_response is None
        return read_response
    
#entity1

@pytest.mark.asyncio
async def test_update_or_create_entity_1():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_not_null_default": "test2"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_not_null_default": "test3"
    })
    assert len(read_reponse) == 0
    create_response = _update_or_create(
        "/entity1", {
                "field_text_primary_not_null_no_default": "pk3"
            }, {
                "field_text_not_null_default": "test3",
                "field_text_primary_not_null_no_default": "pk3",#ids aussi obligatoire dans le corps
                "field_to_join": 1,
                "field_text_creatable_not_updatable": "test",
                "field_text_updatable_not_creatable": "test"
            }
    )
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_not_null_default": "test3"
    })
    assert len(read_reponse) == 1
    read_reponse[0]["field_text_creatable_not_updatable"] == "test"#est créatable, mais pas updatable
    read_reponse[0]["field_text_updatable_not_creatable"] is None#n'est pas créatable, mais updatable
    
    #on appelle le put une deuxième fois
    create_response = _update_or_create(
        "/entity1", {
                "field_text_primary_not_null_no_default": "pk3"
            }, {
                "field_text_not_null_default": "test3",
                "field_text_primary_not_null_no_default": "pk3",#ids aussi obligatoire dans le corps
                "field_to_join": 1,
                "field_text_creatable_not_updatable": "test2",
                "field_text_updatable_not_creatable": "test"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_not_null_default": "test3"
    })
    assert len(read_reponse) == 1
    read_reponse[0]["field_text_creatable_not_updatable"] == "test"#est pas créatable, mais pas updatable
    read_reponse[0]["field_text_updatable_not_creatable"] == "test"#n'est pas créatable, mais updatable

    #on appelle le put une troisième fois
    create_response = _update_or_create(
        "/entity1", {
                "field_text_primary_not_null_no_default": "pk3"
            }, {
                "field_text_not_null_default": "test2",
                "field_text_primary_not_null_no_default": "pk3",#ids aussi obligatoire dans le corps
                "field_to_join": 1,
                "field_text_creatable_not_updatable": "test2",
                "field_text_updatable_not_creatable": "test2"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_not_null_default": "test3"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_not_null_default": "test2"
    })
    assert len(read_reponse) == 2
    read_reponse[0]["field_text_creatable_not_updatable"] == "test"#est pas créatable, mais pas updatable
    read_reponse[1]["field_text_creatable_not_updatable"] == "test"#est pas créatable, mais pas updatable
    read_reponse[0]["field_text_updatable_not_creatable"] == "test2"#n'est pas créatable, mais updatable
    read_reponse[1]["field_text_updatable_not_creatable"] == "test2"#n'est pas créatable, mais updatable



@pytest.mark.asyncio
async def test_update_or_create_entity_25():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    ret = _update_or_create(
        "/entity25", {
                "field_id": 4
            }, {
                "field_id": 4,
                "username": "user2",#sera ignoré parce que not updatable
                "other": 4
            },
            auth=("user1", "test_password")
    )
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 3
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 4
    assert read_reponse[2]["field_id"] == 10
    assert read_reponse[0]["other"] == 1
    assert read_reponse[1]["other"] == 4
    assert read_reponse[2]["other"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

    #une deuxième fois
    ret = _update_or_create(
        "/entity25", {
                "field_id": 4
            }, {
                "field_id": 4,
                "username": "user2",
                "other": 5
            },
            auth=("user1", "test_password")
    )
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 3
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 4
    assert read_reponse[2]["field_id"] == 10
    assert read_reponse[0]["other"] == 1
    assert read_reponse[1]["other"] == 5
    assert read_reponse[2]["other"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

    #une troisième fois
    ret = _update_or_create(
        "/entity25", {
                "field_id": 4
            }, {
                "field_id": 4,
                "username": "user2",
                "other": 6
            },
            auth=("user1", "test_password")
    )
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 3
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 4
    assert read_reponse[2]["field_id"] == 10
    assert read_reponse[0]["other"] == 1
    assert read_reponse[1]["other"] == 6
    assert read_reponse[2]["other"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
