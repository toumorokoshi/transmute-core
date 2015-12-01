import pytest
from marshmallow.exceptions import ValidationError
from web_transmute.compat import string_type


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("-1", -1)
])
def test_int_deserializer_happy(serializer_cache, inp, expected_output):
    """ test all happy cases for the integer serializer """
    serializer = serializer_cache[int]
    assert serializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_int_deserializer_unhappy(serializer_cache, unhappy_input):
    """ test all unhappy cases for the integer serializer """
    serializer = serializer_cache[int]
    with pytest.raises(ValidationError):
        serializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("1.0", 1.0)
])
def test_float_deserializer_happy(serializer_cache, inp, expected_output):
    serializer = serializer_cache[float]
    """ test all happy cases for the integer serializer """
    assert serializer.deserialize(inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_float_deserializer_unhappy(serializer_cache, unhappy_input):
    """ test all unhappy cases for the integer serializer """
    serializer = serializer_cache[float]
    with pytest.raises(ValidationError):
        serializer.deserialize(unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("true", True), ("false", False),
    ("True", True), ("f", False),
])
def test_bool_deserializer_happy(serializer_cache, inp, expected_output):
    serializer = serializer_cache[bool]
    assert serializer.deserialize(inp) is expected_output


@pytest.mark.parametrize("inp, expected_output", [
    ("foo", "foo")
])
def test_string_deserializer_happy(serializer_cache, inp, expected_output):
    serializer = serializer_cache[string_type]
    assert serializer.deserialize(inp) is expected_output
