import pytest
from transmute_core.compat import string_type
from transmute_core.exceptions import SerializationException


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("-1", -1)
])
def test_int_load_happy(serializer, inp, expected_output):
    """ test all happy cases for the integer serializer """
    assert serializer.load(int, inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_int_load_unhappy(serializer, unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializationException):
        serializer.load(int, unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("1.0", 1.0)
])
def test_float_load_happy(serializer, inp, expected_output):
    """ test all happy cases for the integer serializer """
    assert serializer.load(float, inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_float_load_unhappy(serializer, unhappy_input):
    """ test all unhappy cases for the integer serializer """
    with pytest.raises(SerializationException):
        serializer.load(float, unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("true", True), ("false", False),
])
def test_bool_load_happy(serializer, inp, expected_output):
    assert serializer.load(bool, inp) is expected_output


@pytest.mark.parametrize("inp, expected_output", [
    ("foo", "foo")
])
def test_string_load_happy(serializer, inp, expected_output):
    assert serializer.load(string_type, inp) == expected_output
