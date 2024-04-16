from main import create_api
from reinit_db import reinit_db
from fastapi.testclient import TestClient
import pytest
from .test_read import _read

async  def _create(route: str, data: dict, return_code: int = 200):
    with TestClient(await create_api()) as client:
        ret = client.post(route, json=data)
        assert ret.status_code == return_code
        if return_code == 200:
            resp = ret.json()
            print(resp)
            assert resp is None
            return resp
    
@pytest.mark.asyncio
async def test_create():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Les Travailleurs de la Mer"
    })
    assert len(read_reponse) == 0
    create_response = await _create(
        "/book",  {
            "book_id": 3,
            "title": "Les Travailleurs de la Mer",
            "public_domain": True
        }
    )
    read_reponse = await _read("/book", {
        "title": "Les Travailleurs de la Mer"
    })
    assert len(read_reponse) == 1
    entity = read_reponse[0]
    assert entity["book_id"] == 3
    assert entity["title"] == "Les Travailleurs de la Mer"
    assert entity["public_domain"] == True

@pytest.mark.asyncio
async def test_create_already_exist():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Les Travailleurs de la Mer"
    })
    assert len(read_reponse) == 0
    create_response = await _create(
        "/book",  {
            "book_id": 1,
            "title": "Les Travailleurs de la Mer",
            "public_domain": True
        },
        return_code=409
    )
    read_reponse = await _read("/book", {
        "title": "Les Travailleurs de la Mer"
    })
    assert len(read_reponse) == 0