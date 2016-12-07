import pytest
from transmute_core.function import TransmuteFunction
import transmute_core


@transmute_core.describe(paths="/")
@transmute_core.annotate({"return": int})
def raw_func():
    return 12345


@pytest.fixture
def func():
    return TransmuteFunction(raw_func)


def test_callable(func):
    """ test function is callable, and routes to the inner function. """
    assert func() == 12345


def test_return_type(func):
    """ test function is callable, and routes to the inner function. """
    assert func.return_type is int


def test_swagger_schema_has_object(func):
    swagger = func.get_swagger_operation()
    assert swagger.responses["200"].schema.to_primitive() == {
        "title": "SuccessObject",
        "type": "object",
        "required": ["success", "result"],
        "properties": {
            "success": {"type": "boolean"},
            "result": {"type": "number"}
        }
    }


def test_swagger_schema_path(func):
    swagger = func.get_swagger_path()
    assert swagger.get.responses["200"].schema.to_primitive() == {
        "title": "SuccessObject",
        "type": "object",
        "required": ["success", "result"],
        "properties": {
            "success": {"type": "boolean"},
            "result": {"type": "number"}
        }
    }


def test_function_raises_exception_on_path_missing():

    @transmute_core.describe(paths=[])
    def func():
        pass

    with pytest.raises(transmute_core.InvalidTransmuteDefinition):
        TransmuteFunction(func)
