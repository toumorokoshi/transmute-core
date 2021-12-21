import pytest
import sys


def pytest_ignore_collect(*args, **kwargs):
    if sys.version_info < (3, 5):
        return True
    return False


@pytest.fixture
def app(loop):
    from .example import create_app

    return create_app()


@pytest.fixture
def cli(app, loop, test_client):
    return loop.run_until_complete(test_client(app))
