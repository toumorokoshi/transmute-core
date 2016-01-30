import pytest
from marshmallow.exceptions import ValidationError
from web_transmute.compat import string_type


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("-1", -1)
])
def test_int_load_happy(serializer_cache, inp, expected_output):
    """ test all happy cases for the integer serializer """
    serializer = serializer_cache[int]
    assert serializer.load(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_int_load_unhappy(serializer_cache, unhappy_input):
    """ test all unhappy cases for the integer serializer """
    serializer = serializer_cache[int]
    with pytest.raises(ValidationError):
        serializer.load(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("1.0", 1.0)
])
def test_float_load_happy(serializer_cache, inp, expected_output):
    serializer = serializer_cache[float]
    """ test all happy cases for the integer serializer """
    assert serializer.load(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_float_load_unhappy(serializer_cache, unhappy_input):
    """ test all unhappy cases for the integer serializer """
    serializer = serializer_cache[float]
    with pytest.raises(ValidationError):
        serializer.load(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("true", True), ("false", False),
    ("True", True), ("f", False),
])
def test_bool_load_happy(serializer_cache, inp, expected_output):
    serializer = serializer_cache[bool]
    assert serializer.load(inp) is expected_output


@pytest.mark.parametrize("inp, expected_output", [
    ("foo", "foo")
])
def test_string_load_happy(serializer_cache, inp, expected_output):
    serializer = serializer_cache[string_type]
    assert serializer.load(inp) is expected_output
