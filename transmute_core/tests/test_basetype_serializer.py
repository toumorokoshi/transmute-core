import pytest
from transmute_core.compat import string_type
from transmute_core.exceptions import SerializationException
from datetime import datetime

NOW = datetime.now()


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("-1", -1)
])
def test_int_load_happy(schematics_serializer, inp, expected_output):
    """ test all happy cases for the integer schematics_serializer """
    assert schematics_serializer.load(int, inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_int_load_unhappy(schematics_serializer, unhappy_input):
    """ test all unhappy cases for the integer schematics_serializer """
    with pytest.raises(SerializationException):
        schematics_serializer.load(int, unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("10", 10), ("1.0", 1.0)
])
def test_float_load_happy(schematics_serializer, inp, expected_output):
    """ test all happy cases for the integer schematics_serializer """
    assert schematics_serializer.load(float, inp) == expected_output


@pytest.mark.parametrize("unhappy_input", [
    "foo", "bar"
])
def test_float_load_unhappy(schematics_serializer, unhappy_input):
    """ test all unhappy cases for the integer schematics_serializer """
    with pytest.raises(SerializationException):
        schematics_serializer.load(float, unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [
    ("true", True), ("false", False),
    (True, True), (False, False),
])
def test_bool_load_happy(schematics_serializer, inp, expected_output):
    assert schematics_serializer.load(bool, inp) is expected_output


@pytest.mark.parametrize("inp, expected_output", [
    ("foo", "foo")
])
def test_string_load_happy(schematics_serializer, inp, expected_output):
    assert schematics_serializer.load(string_type, inp) == expected_output


@pytest.mark.parametrize("inp, expected_output", [
    (NOW.isoformat(), NOW)
])
def test_datetime_load_happy(schematics_serializer, inp, expected_output):
    assert schematics_serializer.load(datetime, inp) == expected_output


@pytest.mark.parametrize("inp", [
    ("")
])
def test_datetime_load_unhappy(schematics_serializer, inp):
    with pytest.raises(SerializationException):
        schematics_serializer.load(datetime, inp)
