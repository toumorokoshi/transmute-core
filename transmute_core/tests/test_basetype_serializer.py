import pytest
from transmute_core.compat import string_type
from transmute_core.exceptions import SerializationException
from datetime import datetime

NOW = datetime.now()
UTCNOW = datetime.utcnow()


@pytest.mark.parametrize("inp, expected_output", [("10", 10), ("-1", -1)])
def test_int_load_happy(object_serializer_set, inp, expected_output):
    """test all happy cases for the integer serializer"""
    assert object_serializer_set.load(int, inp) == expected_output


@pytest.mark.parametrize("unhappy_input", ["foo", "bar"])
def test_int_load_unhappy(object_serializer_set, unhappy_input):
    """test all unhappy cases for the integer serializer"""
    with pytest.raises(SerializationException):
        object_serializer_set.load(int, unhappy_input)


@pytest.mark.parametrize("inp, expected_output", [("10", 10), ("1.0", 1.0)])
def test_float_load_happy(object_serializer_set, inp, expected_output):
    """test all happy cases for the integer serializer"""
    assert object_serializer_set.load(float, inp) == expected_output


@pytest.mark.parametrize("unhappy_input", ["foo", "bar"])
def test_float_load_unhappy(object_serializer_set, unhappy_input):
    """test all unhappy cases for the integer serializer"""
    with pytest.raises(SerializationException):
        object_serializer_set.load(float, unhappy_input)


@pytest.mark.parametrize(
    "inp, expected_output",
    [("true", True), ("false", False), (True, True), (False, False)],
)
def test_bool_load_happy(object_serializer_set, inp, expected_output):
    assert object_serializer_set.load(bool, inp) is expected_output


@pytest.mark.parametrize("inp, expected_output", [("foo", "foo")])
def test_string_load_happy(object_serializer_set, inp, expected_output):
    assert object_serializer_set.load(string_type, inp) == expected_output


@pytest.mark.parametrize("inp, expected_output", [(NOW.isoformat(), NOW)])
def test_datetime_load_happy(object_serializer_set, inp, expected_output):
    assert object_serializer_set.load(datetime, inp) == expected_output


@pytest.mark.parametrize("inp, expected_output", [(NOW, NOW.isoformat())])
def test_datetime_dump_unhappy(object_serializer_set, inp, expected_output):
    assert object_serializer_set.dump(datetime, inp) == expected_output


@pytest.mark.parametrize("inp", [("")])
def test_datetime_load_unhappy(object_serializer_set, inp):
    with pytest.raises(SerializationException):
        object_serializer_set.load(datetime, inp)


@pytest.mark.parametrize("inp, out", [(None, None), ("s", "s")])
def test_none_serialzer(object_serializer_set, inp, out):
    assert object_serializer_set.load(None, inp) == out
