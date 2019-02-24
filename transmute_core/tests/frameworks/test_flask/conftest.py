import pytest
from .example import app


@pytest.fixture
def test_app():
    return app.test_client()
