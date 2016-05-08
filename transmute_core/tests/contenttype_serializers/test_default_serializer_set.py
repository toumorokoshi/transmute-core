import pytest
from transmute_core import NoSerializerFound


def test_default_serializer_json(serializer_set):
    frm, expected_to = {"foo": "bar"}, b'{"foo": "bar"}'
    serializer = serializer_set["application/json"]
    assert serializer.dump(frm) == expected_to
    assert serializer.load(expected_to) == frm


def test_default_serializer_yaml(serializer_set):
    frm, expected_to = {"foo": "bar"}, b'foo: bar\n'
    serializer = serializer_set["application/yaml"]
    assert serializer.dump(frm) == expected_to
    assert serializer.load(expected_to) == frm


def test_no_serializer_found_raises_exception(serializer_set):
    with pytest.raises(NoSerializerFound):
        assert serializer_set["oogabooga"]


def test_keys(serializer_set):
    assert serializer_set.keys() == [
        "application/json", "application/x-yaml"
    ]
