from main import create_api
from reinit_db import reinit_db
from fastapi.testclient import TestClient
import pytest

expected_result = [
    {
        "book_id": 1,
        "title": "Cyrano de Bergerac", 
        "public_domain": True
    },
    {
        "book_id": 2,
        "title": "We the Living", 
        "public_domain": False
    }
]

async def _read(route: str, filters: dict, **kwargs):
    with TestClient(await create_api()) as client:
        ret = client.get(route, params=filters, **kwargs)
        assert ret.status_code == 200
        resp = ret.json()
        print(resp)
        assert type(resp) == list
        return resp
    
def _check_read_response(list_row, list_expected_result):
    for row in list_row:
        assert "book_id" in row
        assert "title" in row
        assert "public_domain" in row

        assert type(row["book_id"]) == int
        assert type(row["title"]) == str
        assert type(row["public_domain"]) == bool

        assert any([
            all([k in expected_result and row[k] == expected_result[k] for k in row]) 
            for expected_result in list_expected_result
        ])

    for expected_result in list_expected_result:
        assert expected_result in list_row 
        
       
@pytest.mark.asyncio
async def test_read_no_filter():
    await reinit_db()
    read_response = await _read("/book", {})
    assert len(read_response) == 2
    _check_read_response(read_response, expected_result)

@pytest.mark.asyncio
async def test_read_filter_1():
    await reinit_db()
    read_response = await _read("/book", {"title": "Bergerac"})
    assert len(read_response) == 1
    _check_read_response(read_response, [expected_result[0]])

@pytest.mark.asyncio
async def test_read_filter_2():
    await reinit_db()
    read_response = await _read("/book", {"title": "the"})
    assert len(read_response) == 1
    _check_read_response(read_response, [expected_result[1]])

@pytest.mark.asyncio
async def test_read_forbidden_filter():
    await reinit_db()
    read_response = await _read("/book", {"book_id": 1})#filter is ignored for now (may change in the future)
    assert len(read_response) == 2
    _check_read_response(read_response, expected_result)