import inspect
import pytest

import transmute_core
from transmute_core.function import TransmuteFunction
from transmute_core.http_parameters import Param
from transmute_core.function.signature import Argument
from .conftest import Pet


@transmute_core.describe(paths="/", tags=["example"])
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
    """test function is callable, and routes to the inner function."""
    assert func() == 12345


def test_description(func):
    """description should be the docstring."""
    assert func.description == inspect.cleandoc(raw_func.__doc__)


def test_summary(func):
    """summary should be the first non-empty line in the docstring."""
    assert func.summary == "foo bar"


def test_tags(func):
    assert func.tags == set(["example"])


def test_return_type(func):
    """test function is callable, and routes to the inner function."""
    assert func.get_response_by_code(200) is int


def test_swagger_schema_has_object(func):
    swagger = func.get_swagger_operation()
    assert swagger.responses["200"].schema.to_primitive() == {"type": "integer"}


def test_swagger_operation_has_operation_id(func):
    op = func.get_swagger_operation()
    assert op.operationId == "raw_func"


def test_swagger_operation_has_tags(func):
    op = func.get_swagger_operation()
    assert op.tags == ["example"]


def test_swagger_schema_path(func):
    swagger = func.get_swagger_path()
    assert swagger.get_.responses["200"].schema.to_primitive() == {"type": "integer"}


def test_body_param_func(single_body_transmute_func):
    func = single_body_transmute_func
    assert isinstance(func.parameters.body, Param)
    assert func.parameters.body.argument_name == "body"


def test_function_raises_exception_on_path_missing():
    @transmute_core.describe(paths=[])
    def func():
        pass

    with pytest.raises(transmute_core.InvalidTransmuteDefinition):
        TransmuteFunction(func)
