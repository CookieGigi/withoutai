import pytest


# E2E
@pytest.mark.anyio
async def test_models_config_default_ok(client_default):
    r = await client_default.get("/v1/models/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    assert data["object"] == "list"
    assert data["data"][0]["id"] != ""
    assert data["data"][0]["owned_by"] != ""
    assert data["data"][0]["object"] != ""
