from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db
import json
from .test_read import _read
import pytest

def _delete(route: str, data_ids: dict, **kwargs):
    with TestClient(app) as client:
        ret = client.delete(route, params=data_ids, **kwargs)
        assert ret.status_code == 200
        read_response = ret.json()
        print(read_response)
        assert read_response is None
        return read_response
    
#entity1
@pytest.mark.asyncio
async def test_delete_entity_1_exists():
    await reinit_db()
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1"
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 1
    })
    assert len(read_reponse) == 1
    create_response = _delete(
        "/entity1", {
            "field_text_primary_not_null_no_default": "pk1"
            }
    )
    read_reponse = _read("/entity1", {
        "field_text_primary_not_null_no_default": "pk1"
    })
    assert len(read_reponse) == 0
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 1
    })
    assert len(read_reponse) == 0

@pytest.mark.asyncio
async def test_delete_entity_1_not_exists():
    await reinit_db()
    with TestClient(app) as client:
        ret = client.delete("/entity1", 
                params={
                    "field_text_primary_not_null_no_default": "does_not_exist"
                })
    assert ret.status_code == 404

#entity1
@pytest.mark.asyncio
async def test_soft_delete_entity_6_exists():
    await reinit_db()
    read_reponse = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse) == 1
    create_response = _delete(
        "/entity6", {
            "field_id": 1
        }
    )
    read_reponse = _read("/entity6", {
        "field_id": 1
    })
    assert len(read_reponse) == 0

#TODO : test not exist


#entity14
@pytest.mark.asyncio
async def test_delete_entity_14_exists():
    """
    Le cascade delete fonctionne car relation zero or one
    """
    await reinit_db()
    read_reponse = _read("/entity14", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 3
    })
    assert len(read_reponse) == 0
    create_response = _delete(
        "/entity14", {
            "field_to_join": 3
            }
    )
    read_reponse = _read("/entity14", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 0
    #n'a supprimé que ce qu'on a demandé
    read_reponse = _read("/entity14", {
        "field_to_join": 1
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 3
    })
    assert len(read_reponse) == 0

#entity17
@pytest.mark.asyncio
async def test_delete_entity_17_exists():
    await reinit_db()
    read_reponse = _read("/entity17", {
        "field_to_join": 1
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 1
    })
    assert len(read_reponse) == 1
    create_response = _delete(
        "/entity17", {
            "field_to_join": 1
            }
    )
    read_reponse = _read("/entity17", {
        "field_to_join": 1
    })
    assert len(read_reponse) == 0
    #n'a supprimé que ce qu'on a demandé
    read_reponse = _read("/entity17", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 1
    })
    assert len(read_reponse) == 0

@pytest.mark.asyncio
async def test_delete_entity_17_exists_but_not_link():
    """
    On vérifie que la suppression est atomique : ie, que l'entité n'est pas supprimée si le
    cascade delete d'un lien n'a pas fonctionné.
    Ce qui ne sera effectivement pas le cas ici, car le lien n'existe pas alors que la relation est one
    """
    await reinit_db()
    read_reponse = _read("/entity17", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 3
    })
    assert len(read_reponse) == 0
    with TestClient(app) as client:
        ret = client.delete(
            "/entity17", params={
                "field_to_join": 3
                }
        )
        assert ret.status_code == 404
    #on teste le cascade delete a bien rollback
    read_reponse = _read("/entity17", {
        "field_to_join": 3
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity17", {
        "field_to_join": 1
    })
    assert len(read_reponse) == 1
    read_reponse = _read("/entity3", {
        "field_to_be_joined": 3
    })
    assert len(read_reponse) == 0

#entity1
@pytest.mark.asyncio
async def test_delete_entity_20_exists():
    await reinit_db()
    read_reponse = _read("/entity20", {
        "column_2": "1"
    })
    assert len(read_reponse) == 1
    #on teste le cascade delete
    read_reponse = _read("/entity20", {
        "column_2": "1"
    })
    assert len(read_reponse) == 1
    create_response = _delete(
        "/entity20", {
            "column_2": "1"
        }
    )
    read_reponse = _read("/entity20", {
        "column_2": "1"
    })
    assert len(read_reponse) == 0

@pytest.mark.asyncio
async def test_delete_entity_25_exists():
    await reinit_db()
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_id"] == 1
    assert read_reponse[1]["field_id"] == 10
    assert read_reponse[0]["other"] == 1
    assert read_reponse[1]["other"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2
    
    delete_response = _delete(
        "/entity25", {
            "field_id": 1,
            "username": "user2"
        }, 
        auth=("user1", "test_password")
    )
    read_reponse = _read("/entity25", {}, auth=("user1", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 10
    assert read_reponse[0]["other"] == 10
    read_reponse = _read("/entity25", {}, auth=("user2", "test_password"))
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_id"] == 2

@pytest.mark.asyncio
async def test_delete_entity_27_no_other_id():
    await reinit_db()
    read_reponse = _read("/entity27", {
        "field_1": 1
    })
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_1"] == 1
    assert read_reponse[1]["field_1"] == 1
    assert read_reponse[0]["field_2"] == 1
    assert read_reponse[1]["field_2"] == 2
    
    read_reponse = _read("/entity27", {})
    assert len(read_reponse) == 5
    
    delete_response = _delete(
        "/entity27", {}
    )

    read_reponse = _read("/entity27", {
        "field_1": 1
    })
    assert len(read_reponse) == 0

    read_reponse = _read("/entity27", {})
    assert len(read_reponse) == 3

@pytest.mark.asyncio
async def test_delete_entity_27_other_id():
    await reinit_db()
    read_reponse = _read("/entity27", {
        "field_1": "1"
    })
    assert len(read_reponse) == 2
    assert read_reponse[0]["field_1"] == 1
    assert read_reponse[1]["field_1"] == 1
    assert read_reponse[0]["field_2"] == 1
    assert read_reponse[1]["field_2"] == 2
    
    read_reponse = _read("/entity27", {})
    assert len(read_reponse) == 5
    
    delete_response = _delete(
        "/entity27", {
            "field_2": 1
        }
    )

    read_reponse = _read("/entity27", {
        "field_1": 1
    })
    assert len(read_reponse) == 1
    assert read_reponse[0]["field_1"] == 1
    assert read_reponse[0]["field_2"] == 2

    read_reponse = _read("/entity27", {})
    assert len(read_reponse) == 4
