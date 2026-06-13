import pytest


@pytest.mark.anyio
async def test_root_ok(client):
    r = await client.get("/")
    assert r.status_code == 200
