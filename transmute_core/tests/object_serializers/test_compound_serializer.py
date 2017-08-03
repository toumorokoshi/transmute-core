import pytest
from transmute_core.object_serializers import (
    ListSerializer
)


@pytest.fixture
def list_serializer(object_serializer_set):
    return ListSerializer(object_serializer_set)


def test_list_serializer(list_serializer):
    x = ["10"]

    obj = list_serializer.load([int], x)
    assert obj == [10]
    obj = list_serializer.dump([int], obj)
    assert obj == [10]


def test_list_serializer_json_schema(list_serializer):
    schema = list_serializer.to_json_schema([str])
    assert schema == {
        "type": "array",
        "items": {"type": "string"}
    }


def test_list_serializer_can_handle(list_serializer):
    schema = list_serializer.to_json_schema([str])
    assert schema == {
        "type": "array",
        "items": {"type": "string"}
    }
