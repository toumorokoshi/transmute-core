import inspect
import pytest
from transmute_core.function import TransmuteFunction
import transmute_core


@transmute_core.describe(paths="/")
@transmute_core.annotate({"return": int})
def raw_func():
    """
    foo bar

    baz
    """
    return 12345


@pytest.fixture
def func():
    return TransmuteFunction(raw_func)


def test_callable(func):
    """ test function is callable, and routes to the inner function. """
    assert func() == 12345


def test_description(func):
    """ description should be the docstring. """
    assert func.description == inspect.cleandoc(raw_func.__doc__)


def test_summary(func):
    """ summary should be the first non-empty line in the docstring. """
    assert func.summary == "foo bar"


def test_return_type(func):
    """ test function is callable, and routes to the inner function. """
    assert func.get_response_by_code(200) is int


def test_swagger_schema_has_object(func):
    swagger = func.get_swagger_operation()
    assert swagger.responses["200"].schema.to_primitive() == {
        "type": "number"
    }


def test_swagger_schema_path(func):
    swagger = func.get_swagger_path()
    assert swagger.get.responses["200"].schema.to_primitive() == {
        "type": "number"
    }


def test_function_raises_exception_on_path_missing():

    @transmute_core.describe(paths=[])
    def func():
        pass

    with pytest.raises(transmute_core.InvalidTransmuteDefinition):
        TransmuteFunction(func)
