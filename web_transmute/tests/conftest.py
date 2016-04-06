import pytest
from web_transmute.contenttype_serializers import get_default_serializer_set
from web_transmute.schematics_serializer import SchematicsSerializer


@pytest.fixture
def serializer_set():
    return get_default_serializer_set()


@pytest.fixture
def serializer():
    return SchematicsSerializer()
