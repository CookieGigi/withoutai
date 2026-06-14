import pytest


@pytest.mark.anyio
async def test_models_config_default_ok(client_default):
    r = await client_default.get("/v1/models/")
    assert r.status_code == 200
