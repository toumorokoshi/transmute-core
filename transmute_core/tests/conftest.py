import pytest
from transmute_core import (
    annotate,
    describe,
    default_context,
    get_default_serializer_set,
    get_default_object_serializer_set,
    Response,
    SchematicsSerializer,
    TransmuteFunction,
)
from schematics.models import Model
from schematics.types import StringType, IntType


@pytest.fixture
def context():
    return default_context


@pytest.fixture
def serializer_set():
    return get_default_serializer_set()


@pytest.fixture
def object_serializers():
    return get_default_object_serializer_set()


@pytest.fixture
def object_serializer_set():
    return get_default_object_serializer_set()


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


@pytest.fixture
def transmute_func_custom_code():
    @describe(paths="/api/v1/multiply", success_code=201)
    @annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        return left * right

    return TransmuteFunction(multiply)


@pytest.fixture
def transmute_func_post():
    @describe(paths="/api/v1/multiply", methods=["POST"])
    @annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        return left * right

    return TransmuteFunction(multiply)


class Pet(Model):

    kind = StringType(required=True)
    age = IntType()


@pytest.fixture
def single_body_transmute_func():
    @describe(paths="/", body_parameters="body")
    @annotate({"body": Pet})
    def body_param_func():
        return None

    return TransmuteFunction(body_param_func)


@pytest.fixture
def complex_transmute_func():
    @describe(paths="/api/v1/adopt")
    @annotate({"return": Pet})
    def adopt():
        return Pet({"kind": "dog", "age": 5})

    return TransmuteFunction(adopt)


@pytest.fixture
def response_transmute_func():
    @describe(
        paths="/api/v1/create_if_authorized/",
        response_types={
            401: {"type": str, "description": "unauthorized"},
            201: {"type": bool, "headers": {"location": {"type": str}}},
        },
    )
    @annotate({"username": str})
    def create_if_authorized(username):
        if username != "im the boss":
            return Response("this is unauthorized!", 201)
        else:
            return Response(True, 401)

    return TransmuteFunction(create_if_authorized)
