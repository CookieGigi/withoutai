import pytest
from httpx import AsyncClient, ASGITransport
from src.api.app import create_app

# client to test api
app = create_app()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


# anyio backend — needed for async tests
@pytest.fixture
def anyio_backend():
    return "asyncio"
