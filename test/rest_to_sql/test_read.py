from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db
import json
import pytest


def _read(route: str, filters: dict, **kwargs):
    with TestClient(app) as client:
        ret = client.get(route, params=filters, **kwargs)
        assert ret.status_code == 200
        read_response = ret.json()
        print(read_response)
        assert type(read_response) == list
        return read_response
    

def _check_read_response(list_row):
    for row in list_row:
        assert "field_test" in row
        assert "field_int" in row
        assert "field_text_primary_not_null_no_default" in row
        assert "field_text_not_null_default" in row
        assert "field_text_default" in row
        assert "field_text_no_default" in row
        assert "field_text_overwritten_default" in row
        assert "field_text_not_writable" in row
        assert "field_text_not_writable_no_default" in row
        assert "field_bool_converted" in row
        assert "field_bool_converted_bis" in row
        assert "field_text_creatable_not_updatable" in row
        assert "field_text_updatable_not_creatable" in row
        
        assert "column_to_join" not in row
        assert "column_to_be_joined" not in row

        assert "column_test" not in row
        assert "column_int" not in row
        assert "column_text_primary_not_null_no_default" not in row
        assert "column_text_not_null_default" not in row
        assert "column_text_default" not in row
        assert "column_text_no_default" not in row
        assert "column_text_overwritten_default" not in row
        assert "column_text_not_writable" not in row
        assert "column_text_not_writable_no_default" not in row
        assert "column_text_oui_non" not in row
        assert "column_text_oui_non_bis" not in row
        assert "column_text_not_readable" not in row
        assert "column_text_creatable_not_updatable" not in row
        assert "column_text_updatable_not_creatable" not in row
        assert "field_text_not_readable" not in row

        assert "column_invisible" not in row#TODO : vérifier que pas d'écriture possible

        assert type(row["field_test"]) == str
        assert type(row["field_int"]) == int
        assert type(row["field_text_primary_not_null_no_default"]) == str
        assert type(row["field_text_not_null_default"]) == str
        assert type(row["field_text_default"]) == str
        assert type(row["field_text_no_default"]) == str
        assert type(row["field_text_overwritten_default"]) == str
        assert type(row["field_text_not_writable"]) == str
        assert type(row["field_text_not_writable_no_default"]) == str
        assert type(row["field_text_creatable_not_updatable"]) == str
        assert type(row["field_text_updatable_not_creatable"]) == str
        assert type(row["field_bool_converted"]) == bool
        assert type(row["field_bool_converted_bis"]) == bool
    
#entity1

@pytest.mark.asyncio
async def test_read_entity_1_no_filter():
    await reinit_db()
    read_response = _read("/entity1", {})
    assert len(read_response) == 2
    _check_read_response(read_response)
##equal

@pytest.mark.asyncio
async def test_read_entity_1_filter_equal_1():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_not_null_default": "test"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_text_not_null_default"] == "test"

@pytest.mark.asyncio
async def test_read_entity_1_filter_equal_2():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_not_null_default": "test2"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_text_not_null_default"] == "test2"

@pytest.mark.asyncio
async def test_read_entity_1_filter_equal_3():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_not_null_default": "2"
    })
    assert len(read_response) == 0

@pytest.mark.asyncio
async def test_read_entity_1_filter_equal_4():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_not_null_default": "%test%"
    })
    assert len(read_response) == 0
##contain

@pytest.mark.asyncio
async def test_read_entity_1_filter_contain_1():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_text_primary_not_null_no_default"] == "pk1"

@pytest.mark.asyncio
async def test_read_entity_1_filter_contain_2():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk2"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_text_primary_not_null_no_default"] == "pk2"

@pytest.mark.asyncio
async def test_read_entity_1_filter_contain_3():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_primary_not_null_no_default": "3"
    })
    assert len(read_response) == 0

@pytest.mark.asyncio
async def test_read_entity_1_filter_contain_4():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk"
    })
    assert len(read_response) == 2
    _check_read_response(read_response)

@pytest.mark.asyncio
async def test_read_entity_1_filter_contain_5():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_primary_not_null_no_default": "%pk%"
    })
    assert len(read_response) == 2#TODO : contain n'est pas exactement un contain. Ici devrait être 0

@pytest.mark.asyncio
async def test_read_entity_1_filter_joined():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_bool_converted_bis_equal": True#force_long_name
    })
    assert len(read_response) == 1
##pattern

@pytest.mark.asyncio
async def test_read_entity_1_filter_pattern_1():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_default": "other_test"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_text_default"] == "other_test"

@pytest.mark.asyncio
async def test_read_entity_1_filter_pattern_2():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_default": "other_test_2"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_text_default"] == "other_test_2"

@pytest.mark.asyncio
async def test_read_entity_1_filter_pattern_3():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_default": "3"
    })
    assert len(read_response) == 0

@pytest.mark.asyncio
async def test_read_entity_1_filter_pattern_4():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_default": "%other_test%"
    })
    assert len(read_response) == 2
    _check_read_response(read_response)

@pytest.mark.asyncio
async def test_read_entity_1_filter_pattern_5():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_text_default": "%3%"
    })
    assert len(read_response) == 0
##converted

@pytest.mark.asyncio
async def test_read_entity_1_filter_converted_1():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_bool_converted": True
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_bool_converted"] == True

@pytest.mark.asyncio
async def test_read_entity_1_filter_converted_2():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_bool_converted": False
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_bool_converted"] == False
#several
##converted

@pytest.mark.asyncio
async def test_read_entity_1_filter_several_1():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_bool_converted": True,
        "field_text_primary_not_null_no_default": "pk1"
    })
    assert len(read_response) == 1
    _check_read_response(read_response)
    assert read_response[0]["field_bool_converted"] == True
    assert read_response[0]["field_text_primary_not_null_no_default"] == "pk1"

@pytest.mark.asyncio
async def test_read_entity_1_filter_several_2():
    await reinit_db()
    read_response = _read("/entity1", {
        "field_bool_converted": False,
        "field_text_primary_not_null_no_default": "pk1"
    })
    assert len(read_response) == 0


#entity4

@pytest.mark.asyncio
async def test_read_entity_4_no_filter():
    await reinit_db()
    read_response = _read("/entity4", {})
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_id" in row
    assert "field_byte" in row
    assert type(row["field_id"]) == int
    assert type(row["field_byte"]) == str
    assert row["field_byte"] == "some bytes"

#entity5
"""
@pytest.mark.asyncio
async def test_read_entity_5_no_filter():
    await reinit_db()
    read_response = _read("/entity5", {})
    assert len(read_response) == 1#une seule réponse car filtre custom sur is_deleted
    row = read_response[0]
    assert "field_id" in row
    assert "is_deleted" in row
    assert type(row["field_id"]) == int
    assert type(row["is_deleted"]) == bool
    assert row["is_deleted"] == False"""

#entity6

@pytest.mark.asyncio
async def test_read_entity_6_no_filter():
    await reinit_db()
    read_response = _read("/entity6", {})
    assert len(read_response) == 1#une seule réponse car fsoft delete
    row = read_response[0]
    assert "field_id" in row
    assert "is_deleted" not in row
    assert "is_active" in row
    assert type(row["field_id"]) == int

#entity7

@pytest.mark.asyncio
async def test_read_entity_7_no_filter():
    await reinit_db()
    read_response = _read("/entity7", {})
    assert len(read_response) == 4
    for row in read_response:
        assert "column_id" in row
        assert "sort1" in row
        assert "sort2" in row
        assert type(row["column_id"]) == int
        assert type(row["sort1"]) == int
        assert type(row["sort2"]) == int
    #on vérifie l'ordre
    assert read_response[0]["column_id"] == 2
    assert read_response[1]["column_id"] == 1
    assert read_response[2]["column_id"] == 4
    assert read_response[3]["column_id"] == 3

#entity7_bis

@pytest.mark.asyncio
async def test_read_entity_7_bis_no_filter():
    await reinit_db()
    read_response = _read("/entity7_bis", {})
    assert len(read_response) == 4
    for row in read_response:
        assert "column_id" in row
        assert "sort1" in row
        assert "sort2" in row
        assert type(row["column_id"]) == int
        assert type(row["sort1"]) == int
        assert type(row["sort2"]) == int
    #on vérifie l'ordre
    assert read_response[0]["column_id"] == 1
    assert read_response[1]["column_id"] == 2
    assert read_response[2]["column_id"] == 3
    assert read_response[3]["column_id"] == 4
    
#entity11

@pytest.mark.asyncio
async def test_read_entity_11_no_filter():
    await reinit_db()
    read_response = _read("/entity11", {})
    assert len(read_response) == 1#une seule réponse car filtre en dur
    row = read_response[0]
    assert "field_id" in row
    assert "field_to_filter_1" in row
    assert "field_to_filter_2" in row
    assert row["field_to_filter_2"] == "test"


@pytest.mark.asyncio
async def test_read_entity_11_filter():
    await reinit_db()
    read_response = _read("/entity11", {
        "field_to_filter_2":  "test2"
    })
    assert len(read_response) == 0#zero réponse car filtre en dur


@pytest.mark.asyncio
async def test_read_entity_11_filter_2():
    await reinit_db()
    read_response = _read("/entity11", {
        "field_to_filter_1":  "test2"
    })
    assert len(read_response) == 0#zero réponse car filtre en dur

#entity12

@pytest.mark.asyncio
async def test_read_entity_12_no_filter():
    await reinit_db()
    read_response = _read("/entity12", {})
    assert len(read_response) == 2


@pytest.mark.asyncio
async def test_read_entity_12_filter_1():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_min": "2023-03-19T00:00:00"
    })
    assert len(read_response) == 2
    row = read_response[0]
    assert "field_id" in row
    assert "field_date" in row
    assert row["field_date"] == "2023-03-25T00:00:00"
    row = read_response[1]
    assert "field_id" in row
    assert "field_date" in row
    assert row["field_date"] == "2023-03-20T00:00:00"


@pytest.mark.asyncio
async def test_read_entity_12_filter_2():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_min": "2023-03-21T00:00:00"
    })
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_id" in row
    assert "field_date" in row
    assert row["field_date"] == "2023-03-25T00:00:00"


@pytest.mark.asyncio
async def test_read_entity_12_filter_3():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_max": "2023-03-26T00:00:00"
    })
    assert len(read_response) == 2


@pytest.mark.asyncio
async def test_read_entity_12_filter_4():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_max": "2023-03-24T00:00:00"
    })
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_id" in row
    assert "field_date" in row
    assert row["field_date"] == "2023-03-20T00:00:00"


@pytest.mark.asyncio
async def test_read_entity_12_filter_5():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_min": "2023-03-19T00:00:00",
        "field_date_max": "2023-03-24T00:00:00"
    })
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_id" in row
    assert "field_date" in row
    assert row["field_date"] == "2023-03-20T00:00:00"


@pytest.mark.asyncio
async def test_read_entity_12_filter_6():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_min": "2023-03-21T00:00:00",
        "field_date_max": "2023-03-24T00:00:00"
    })
    assert len(read_response) == 0


@pytest.mark.asyncio
async def test_read_entity_12_filter_7():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_min": "2023-03-21T00:00:00",
        "field_date_max": "2023-03-26T00:00:00"
    })
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_id" in row
    assert "field_date" in row
    assert row["field_date"] == "2023-03-25T00:00:00"


@pytest.mark.asyncio
async def test_read_entity_12_filter_6():
    await reinit_db()
    read_response = _read("/entity12", {
        "field_date_min": "2023-03-19T00:00:00",
        "field_date_max": "2023-03-26T00:00:00"
    })
    assert len(read_response) == 2


@pytest.mark.asyncio
async def test_read_entity_13_no_filter_1():
    await reinit_db()
    read_response = _read("/entity13", {})
    assert len(read_response) == 2#distinct
    row = read_response[0]
    assert "field_test" in row
    assert row["field_test"] == "test"
    row = read_response[1]
    assert "field_test" in row
    assert row["field_test"] == "test2"


@pytest.mark.asyncio
async def test_read_entity_16_1():
    await reinit_db()
    read_response = _read("/entity16", {"field_id": 1})
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_test" in row
    assert row["field_test"] == "test"#default


@pytest.mark.asyncio
async def test_read_entity_16_2():
    await reinit_db()
    read_response = _read("/entity16", {"field_id": 2})
    assert len(read_response) == 0


@pytest.mark.asyncio
async def test_read_entity_16_3():
    await reinit_db()
    read_response = _read("/entity16", {"field_id": 2, "field_test": "test2"})
    assert len(read_response) == 1
    row = read_response[0]
    assert "field_test" in row
    assert row["field_test"] == "test2"

#entity15

@pytest.mark.asyncio
async def test_read_entity_15_no_user():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity15", params={})
    assert ret.status_code == 401


@pytest.mark.asyncio
async def test_read_entity_15_bad_password():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity15", params={}, auth=("user1", "wrong_password"))
    assert ret.status_code == 401


@pytest.mark.asyncio
async def test_read_entity_15_good_user():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity15", params={}, auth=("user1", "test_password"))
    data = ret.json()
    assert type(data) == list
    assert len(data) == 1
    row = data[0]
    assert row["field_id"] == 1
    assert row["table_user.column_id"] == 10
    assert row["other"] == '1'#celui sur table_user et non table15


@pytest.mark.asyncio
async def test_read_entity_15_good_user_2():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity15", params={}, auth=("user2", "test_password"))
    data = ret.json()
    assert type(data) == list
    assert len(data) == 1
    row = data[0]
    assert row["field_id"] == 2
    assert row["table_user.column_id"] == 20
    assert row["other"] == '2'#celui sur table_user et non table15


@pytest.mark.asyncio
async def test_read_entity_15_good_user_3():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity15", params={}, auth=("does_not_exist", "test_password"))
    data = ret.json()
    assert type(data) == list
    assert len(data) == 0

@pytest.mark.asyncio
async def test_read_entity_15_good_user_diffrent_in_params():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity15", params={"username": "user2"}, auth=("user1", "test_password"))
    data = ret.json()
    assert type(data) == list
    assert len(data) == 1
    row = data[0]
    assert row["field_id"] == 1#celui de user1, pas user2
    assert row["table_user.column_id"] == 10
    assert row["other"] == '1'#celui sur table_user et non table15

@pytest.mark.asyncio
async def test_read_entity_19_no_option():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity19", params={"add_fixed": False})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 3


@pytest.mark.asyncio
async def test_read_entity_19_option():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity19", params={"add_fixed": True})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 4

@pytest.mark.asyncio
async def test_read_entity_20():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity20", params={})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 5
    for row in data:
        assert "column_1" in row
        assert "column_2" in row
        assert "group" in row
        assert type(row["group"]) == list
        for g in row["group"]:
            assert "table_many.column_1" in g
            assert "table_many.column_2" in g

    assert data[0]["column_1"] == "1"
    assert data[0]["column_2"] == "1"
    assert len(data[0]["group"]) == 1
    assert data[0]["group"][0]["table_many.column_1"] == "1"
    assert data[0]["group"][0]["table_many.column_2"] == "10"

    assert data[1]["column_1"] == "2"
    assert data[1]["column_2"] == "2"
    assert len(data[1]["group"]) == 3
    assert data[1]["group"][0]["table_many.column_1"] == "2"
    assert data[1]["group"][0]["table_many.column_2"] == "20"
    assert data[1]["group"][1]["table_many.column_1"] == "2"
    assert data[1]["group"][1]["table_many.column_2"] == "20"
    assert data[1]["group"][2]["table_many.column_1"] == "2"
    assert data[1]["group"][2]["table_many.column_2"] == "20"

    assert data[2]["column_1"] == "3"
    assert data[2]["column_2"] == "3"
    assert len(data[2]["group"]) == 1
    assert data[2]["group"][0]["table_many.column_1"] == "3"
    assert data[2]["group"][0]["table_many.column_2"] == "30"

    assert data[3]["column_1"] == "3"
    assert data[3]["column_2"] == "3_bis"
    assert len(data[3]["group"]) == 1
    assert data[3]["group"][0]["table_many.column_1"] == "3"
    assert data[3]["group"][0]["table_many.column_2"] == "30"

    assert data[4]["column_1"] == "4"
    assert data[4]["column_2"] == "4"
    assert len(data[4]["group"]) == 0

@pytest.mark.asyncio
async def test_read_entity_20_1():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity20", params={"extend_group": False})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 5
    for row in data:
        assert "column_1" in row
        assert "column_2" in row
        assert "group" in row
        assert row["group"] is None

@pytest.mark.asyncio
async def test_read_entity_22():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity22", params={})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 2
    for row in data:
        assert "field_id" in row
        assert "user_id" in row
        assert "user" in row
        assert type(row["user"]) == dict
        assert "table_user.column_id" in row["user"]
        assert "other" in row["user"]
    assert data[0]["user"]["table_user.column_id"] == 20
    assert data[0]["user"]["other"] == "2"
    assert data[1]["user"]["table_user.column_id"] == 10
    assert data[1]["user"]["other"] == "1"

@pytest.mark.asyncio
async def test_read_entity_22_1():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity22", params={"extend_user": False})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 2
    for row in data:
        assert "field_id" in row
        assert "user_id" in row
        assert "user" in row
        assert row["user"] is None

@pytest.mark.asyncio
async def test_read_entity_23():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity23", params={})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 4
    for row in data:
        assert "column_1" in row
        assert "column_2_bis" in row
        assert "group_bis" in row
        assert type(row["group_bis"]) == list
        for g_bis in row["group_bis"]:
            assert "table20.column_1" in g_bis
            assert "column_2" in g_bis
            assert "group" in g_bis
            for g in g_bis["group"]:
                assert "table_many.column_1" in g
                assert "table_many.column_2" in g

    data[0]["column_1"] == "1"
    data[0]["column_2_bis"] == "1"
    assert len(data[0]["group_bis"]) == 1
    assert data[0]["group_bis"][0]["table20.column_1"] == "1"
    assert data[0]["group_bis"][0]["column_2"] == "1"
    assert len(data[0]["group_bis"][0]["group"]) == 1
    assert data[0]["group_bis"][0]["group"][0]["table_many.column_1"] == "1"
    assert data[0]["group_bis"][0]["group"][0]["table_many.column_2"] == "10"

    data[1]["column_1"] == "2"
    data[1]["column_2_bis"] == "2"
    assert len(data[1]["group_bis"]) == 1
    assert data[1]["group_bis"][0]["table20.column_1"] == "2"
    assert data[1]["group_bis"][0]["column_2"] == "2"
    assert len(data[1]["group_bis"][0]["group"]) == 3
    assert data[1]["group_bis"][0]["group"][0]["table_many.column_1"] == "2"
    assert data[1]["group_bis"][0]["group"][0]["table_many.column_2"] == "20"
    assert data[1]["group_bis"][0]["group"][1]["table_many.column_1"] == "2"
    assert data[1]["group_bis"][0]["group"][1]["table_many.column_2"] == "20"
    assert data[1]["group_bis"][0]["group"][2]["table_many.column_1"] == "2"
    assert data[1]["group_bis"][0]["group"][2]["table_many.column_2"] == "20"

    data[2]["column_1"] == "3"
    data[2]["column_2_bis"] == "3"
    assert len(data[2]["group_bis"]) == 2
    assert data[2]["group_bis"][0]["table20.column_1"] == "3"
    assert data[2]["group_bis"][0]["column_2"] == "3"
    assert len(data[2]["group_bis"][0]["group"]) == 1
    assert data[2]["group_bis"][0]["group"][0]["table_many.column_1"] == "3"
    assert data[2]["group_bis"][0]["group"][0]["table_many.column_2"] == "30"

    assert data[2]["group_bis"][1]["table20.column_1"] == "3"
    assert data[2]["group_bis"][1]["column_2"] == "3_bis"
    assert len(data[2]["group_bis"][1]["group"]) == 1
    assert data[2]["group_bis"][1]["group"][0]["table_many.column_1"] == "3"
    assert data[2]["group_bis"][1]["group"][0]["table_many.column_2"] == "30"

    data[3]["column_1"] == "4"
    data[3]["column_2_bis"] == "4"
    assert len(data[3]["group_bis"]) == 1
    assert data[3]["group_bis"][0]["table20.column_1"] == "4"
    assert data[3]["group_bis"][0]["column_2"] == "4"
    assert len(data[3]["group_bis"][0]["group"]) == 0

@pytest.mark.asyncio
async def test_read_entity_23_1():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity23", params={"extend_group": False, "extend_group_bis": False})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 4
    for row in data:
        assert "column_1" in row
        assert "column_2_bis" in row
        assert "group_bis" in row
        assert row["group_bis"] is None

@pytest.mark.asyncio
async def test_read_entity_23_2():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity23", params={"extend_group": False, "extend_group_bis": True})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 4
    for row in data:
        assert "column_1" in row
        assert "column_2_bis" in row
        assert "group_bis" in row
        assert type(row["group_bis"]) == list
        for g_bis in row["group_bis"]:
            assert "table20.column_1" in g_bis
            assert "column_2" in g_bis
            assert "group" in g_bis
            assert g_bis["group"] is None

    data[0]["column_1"] == "1"
    data[0]["column_2_bis"] == "1"
    assert len(data[0]["group_bis"]) == 1
    assert data[0]["group_bis"][0]["table20.column_1"] == "1"
    assert data[0]["group_bis"][0]["column_2"] == "1"

    data[1]["column_1"] == "2"
    data[1]["column_2_bis"] == "2"
    assert len(data[1]["group_bis"]) == 1
    assert data[1]["group_bis"][0]["table20.column_1"] == "2"
    assert data[1]["group_bis"][0]["column_2"] == "2"

    data[2]["column_1"] == "3"
    data[2]["column_2_bis"] == "3"
    assert len(data[2]["group_bis"]) == 2
    assert data[2]["group_bis"][0]["table20.column_1"] == "3"
    assert data[2]["group_bis"][0]["column_2"] == "3_bis"
    assert data[2]["group_bis"][1]["table20.column_1"] == "3"
    assert data[2]["group_bis"][1]["column_2"] == "3"


    data[3]["column_1"] == "4"
    data[3]["column_2_bis"] == "4"
    assert len(data[3]["group_bis"]) == 1
    assert data[3]["group_bis"][0]["table20.column_1"] == "4"
    assert data[3]["group_bis"][0]["column_2"] == "4"

@pytest.mark.asyncio
async def test_read_limit():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.get("/entity26")
    data = ret.json()
    assert type(data) == list
    assert len(data) == 5

    with TestClient(app) as client:
        ret = client.get("/entity26", params={"limit": 1})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 1
    assert data[0]["field_1"] == 1

    with TestClient(app) as client:
        ret = client.get("/entity26", params={"limit": 3})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 3
    assert data[0]["field_1"] == 1
    assert data[1]["field_1"] == 2
    assert data[2]["field_1"] == 3

    with TestClient(app) as client:
        ret = client.get("/entity26", params={"limit": 100})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 5

    with TestClient(app) as client:
        ret = client.get("/entity26", params={"offset": 1})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 4
    assert data[0]["field_1"] == 2
    assert data[1]["field_1"] == 3
    assert data[2]["field_1"] == 4
    assert data[3]["field_1"] == 5

    with TestClient(app) as client:
        ret = client.get("/entity26", params={"limit": 1, "offset": 1})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 1
    assert data[0]["field_1"] == 2

    with TestClient(app) as client:
        ret = client.get("/entity26", params={"limit": 3, "offset": 1})
    data = ret.json()
    assert type(data) == list
    assert len(data) == 3
    assert data[0]["field_1"] == 2
    assert data[1]["field_1"] == 3
    assert data[2]["field_1"] == 4