import pytest
from transmute_core import (
    annotate, describe,
    default_context,
    SchematicsSerializer,
    get_default_serializer_set,
    ResponseShapeComplex,
    TransmuteFunction
)
from schematics.models import Model
from schematics.types import StringType, IntType


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


class Pet(Model):

    kind = StringType(required=True)
    age = IntType()


@pytest.fixture
def complex_transmute_func():

    @describe(paths="/api/v1/adopt")
    @annotate({"return": Pet})
    def adopt():
        return Pet({
            "kind": "dog",
            "age": 5
        })

    return TransmuteFunction(adopt)
