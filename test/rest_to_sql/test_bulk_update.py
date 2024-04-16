from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db
import json
from .test_read import _read
import pytest
from .test_create import _create
from datetime import datetime, timedelta

def _bulk_update(route: str, data_list: list, **kwargs):
    with TestClient(app) as client:
        ret = client.patch(route, json=data_list, **kwargs)
        return ret
    
#entity1

@pytest.mark.asyncio
async def test_bulk_update_entity_1_ok():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test_10"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2",
        "field_text_default": "other_test_2"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2",
        "field_text_default": "other_test_20"
    })
    assert len(read_reponse) == 0
    ret = _bulk_update(
        "/entity1/bulk", 
        [
            {
                "ids": {"field_text_primary_not_null_no_default": "pk1"},
                "fields_to_update": {"field_text_default": "other_test_10"},
                "options": {}
            },
            {
                "ids": {"field_text_primary_not_null_no_default": "pk2"},
                "fields_to_update": {"field_text_default": "other_test_20"},
                "options": {}
            }
        ]
    )
    assert ret.status_code == 200
    data = ret.json()
    assert data is None
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test_1"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test_10"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2",
        "field_text_default": "other_test_2"
    })
    assert len(read_reponse) == 0
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2",
        "field_text_default": "other_test_20"
    })
    assert len(read_reponse) == 1

@pytest.mark.asyncio
async def test_bulk_update_entity_1_nok():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk3"
    })
    assert len(read_reponse) == 0
    ret = _bulk_update(
        "/entity1/bulk", 
        [
            {
                "ids": {"field_text_primary_not_null_no_default": "pk1"},
                "fields_to_update": {"field_text_default": "other_test_10"},
                "options": {}
            },
            {
                "ids": {"field_text_primary_not_null_no_default": "pk3"},
                "fields_to_update": {"field_text_default": "other_test_30"},
                "options": {}
            }
        ]
    )
    assert ret.status_code == 400
    data = ret.json()
    assert type(data) == dict
    assert "detail" in data
    data = data["detail"]
    assert type(data) == list
    assert len(data) == 1
    data = data[0]
    assert type(data) == dict
    assert "http_status" in data
    assert "detail" in data
    assert data["http_status"] == 404
    assert data["detail"] == "The entity {'field_text_primary_not_null_no_default': 'pk3'} does not exist"
    
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test"
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1",
        "field_text_default": "other_test_10"
    })
    assert len(read_reponse) == 0


@pytest.mark.asyncio
async def test_bulk_update_entity_25_no_password():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    ret = _bulk_update(
        "/entity25/bulk", 
        [
            {
                "ids": {"field_id": 1},
                "fields_to_update": {"field_id": 4},
                "options": {}
            },
            {
                "ids": {"field_id": 10},
                "fields_to_update": {"field_id": 5},
                "options": {}
            }
        ]
    )
    assert ret.status_code == 401
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_bulk_update_entity_25_bad_password():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    ret = _bulk_update(
        "/entity25/bulk", 
        [
            {
                "ids": {"field_id": 1},
                "fields_to_update": {"field_id": 4},
                "options": {}
            },
            {
                "ids": {"field_id": 10},
                "fields_to_update": {"field_id": 5},
                "options": {}
            }
        ],
        auth=("user1", "bad_password")
    )
    assert ret.status_code == 401
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_bulk_update_entity_25_bad_user():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    ret = _bulk_update(
        "/entity25/bulk", 
        [
            {
                "ids": {"field_id": 1},
                "fields_to_update": {"field_id": 4},
                "options": {}
            },
            {
                "ids": {"field_id": 10},
                "fields_to_update": {"field_id": 5},
                "options": {}
            }
        ],
        auth=("does_not_exist", "test_password")
    )
    assert ret.status_code == 400
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_bulk_update_entity_25_good_1():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    ret = _bulk_update(
        "/entity25/bulk", 
        [
            {
                "ids": {"field_id": 1},
                "fields_to_update": {"field_id": 4},
                "options": {}
            },
            {
                "ids": {"field_id": 10},
                "fields_to_update": {"field_id": 5},
                "options": {}
            }
        ],
        auth=("user1", "test_password")
    )
    assert ret.status_code == 200
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 4
    assert read_reponse[1]["field_id"] == 5
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_bulk_update_entity_25_good_2():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    ret = _bulk_update(
        "/entity25/bulk", 
        [
            {
                "ids": {"field_id": 1},
                "fields_to_update": {"field_id": 4},
                "options": {}
            }
        ],
        auth=("user1", "test_password")
    )
    assert ret.status_code == 200
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 4
    assert read_reponse[1]["field_id"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2