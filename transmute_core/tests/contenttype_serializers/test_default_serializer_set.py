import pytest
from transmute_core.contenttype_serializers.serializer_set import NoSerializerFound


def test_default_serializer_json(serializer_set):
    frm, expected_to = {"foo": "bar"}, b'{"foo": "bar"}'
    assert serializer_set.to_type("application/json", frm) == expected_to
    assert serializer_set.from_type("application/json", expected_to) == frm


def test_default_serializer_yaml(serializer_set):
    frm, expected_to = {"foo": "bar"}, b'foo: bar\n'
    assert serializer_set.to_type("application/yaml", frm) == expected_to
    assert serializer_set.from_type("application/yaml", expected_to) == frm


def test_no_serializer_fonud_raises_exception(serializer_set):
    frm, _to = {"foo": "bar"}, b'foo: bar\n'
    with pytest.raises(NoSerializerFound):
        assert serializer_set.to_type("oogabooga", frm)

    with pytest.raises(NoSerializerFound):
        assert serializer_set.from_type("oogabooga", _to)
