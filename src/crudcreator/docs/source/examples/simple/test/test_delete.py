from main import create_api
from reinit_db import reinit_db
from fastapi.testclient import TestClient
import pytest
from .test_read import _read

async def _delete(route: str, data_ids: dict, return_code: int = 200):
    with TestClient(await create_api()) as client:
        ret = client.delete(route, params=data_ids)
        assert ret.status_code == return_code
        if return_code == 200:
            resp = ret.json()
            print(resp)
            assert resp is None
            return resp
    
@pytest.mark.asyncio
async def test_delete():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 1
    delete_response = await _delete(
        "/book", {
            "book_id": 1
        }
    )
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 0

@pytest.mark.asyncio
async def test_delete_entity_not_exists():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 1
    delete_response = await _delete(
        "/book", {
            "book_id": 3
        },
        return_code=404
    )
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 1
    