import pytest
from transmute_core.contenttype_serializers import get_default_serializer_set
from transmute_core.object_serializers import SchematicsSerializer
from transmute_core.function import TransmuteFunction
from transmute_core import annotate, describe


@pytest.fixture
def serializer_set():
    return get_default_serializer_set()


@pytest.fixture
def serializer():
    return SchematicsSerializer()


@pytest.fixture
def transmute_func():

    @describe(paths="/api/v1/multiply")
    @annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        return left * right

    return TransmuteFunction(multiply)
