import pytest
from transmute_core.object_serializers import (
    ListSerializer
)


def test_list_serializer(object_serializer_set):
    x = ["10"]

    obj = object_serializer_set.load([int], x)
    assert obj == [10]
    obj = object_serializer_set.dump([int], obj)
    assert obj == [10]


def test_list_serializer_json_schema(object_serializer_set):
    schema = object_serializer_set.to_json_schema([str])
    assert schema == {
        "type": "array",
        "items": {"type": "string"}
    }


def test_object_serializer_set_can_handle(object_serializer_set):
    schema = object_serializer_set.to_json_schema([str])
    assert schema == {
        "type": "array",
        "items": {"type": "string"}
    }
