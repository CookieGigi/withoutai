import pytest

from .configs import client_default  # noqa: F401


# anyio backend — needed for async tests
@pytest.fixture
def anyio_backend():
    return "asyncio"
