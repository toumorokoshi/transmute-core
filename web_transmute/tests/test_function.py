import pytest
from web_transmute.function import TransmuteFunction
import web_transmute


@web_transmute.annotate({"return": int})
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
