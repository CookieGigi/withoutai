import pytest
from httpx import AsyncClient, ASGITransport
from api import create_app
from containers import InfraContainer, AppContainer

app_container = AppContainer(infra=InfraContainer())
app_container.wire(packages=["api"])
app = create_app()
app.container = app_container


@pytest.fixture
async def client_default():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
