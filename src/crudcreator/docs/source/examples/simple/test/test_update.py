from main import create_api
from reinit_db import reinit_db
from fastapi.testclient import TestClient
import pytest
from .test_read import _read

async def _update(route: str, date_ids: dict, data: dict, return_code: int = 200):
    with TestClient(await create_api()) as client:
        ret = client.patch(route, params=date_ids, json=data)
        assert ret.status_code == return_code
        if return_code == 200:
            resp = ret.json()
            print(resp)
            assert resp is None
            return resp

@pytest.mark.asyncio
async def test_update():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 1
    read_reponse = await _read("/book", {
        "title": "Berge Ressac"
    })
    assert len(read_reponse) == 0
    update_response = await _update(
        "/book", {
                "book_id": 1
            }, {
                "title": "Cyrano de Berge Ressac"
            }
    )
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 0
    read_reponse = await _read("/book", {
        "title": "Berge Ressac"
    })
    assert len(read_reponse) == 1

@pytest.mark.asyncio
async def test_update_already_exist():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 1
    read_reponse[0]["book_id"] == 1
    read_reponse = await _read("/book", {
        "title": "Living"
    })
    assert len(read_reponse) == 1
    read_reponse[0]["book_id"] == 2
    assert len(read_reponse) == 1
    update_response = await _update(
        "/book", {
                "book_id": 1
            }, {
                "book_id": 2
            },
        return_code=409
    )
    read_reponse = await _read("/book", {
        "title": "Bergerac"
    })
    assert len(read_reponse) == 1
    read_reponse[0]["book_id"] == 1
    read_reponse = await _read("/book", {
        "title": "Living"
    })
    assert len(read_reponse) == 1
    read_reponse[0]["book_id"] == 2


@pytest.mark.asyncio
async def test_update_already_exist():
    await reinit_db()
    read_reponse = await _read("/book", {
        "title": "Les Travailleurs de la Mer"
    })
    assert len(read_reponse) == 0
    update_response = await _update(
        "/book", {
                "book_id": 3
            }, {
                "title": "Les Travailleurs de la Mer"
            },
        return_code=404
    )
    read_reponse = await _read("/book", {
        "title": "Les Travailleurs de la Mer"
    })
    assert len(read_reponse) == 0