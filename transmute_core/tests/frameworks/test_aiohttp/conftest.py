import pytest
from .example import create_app


@pytest.fixture
def app(loop):
    return create_app()


@pytest.fixture
def cli(app, loop, test_client):
    return loop.run_until_complete(test_client(app))