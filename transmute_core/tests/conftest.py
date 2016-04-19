import pytest
from transmute_core.contenttype_serializers import get_default_serializer_set
from transmute_core.schematics_serializer import SchematicsSerializer


@pytest.fixture
def serializer_set():
    return get_default_serializer_set()


@pytest.fixture
def serializer():
    return SchematicsSerializer()
