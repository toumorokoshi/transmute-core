import pytest
from web_transmute.serializer_cache import SerializerCache


@pytest.fixture
def serializer_cache():
    return SerializerCache()
