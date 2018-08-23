import pytest
from transmute_core.object_serializers import ListSerializer
from typing import List


def test_list_serializer(object_serializer_set):
    x = ["10"]

    obj = object_serializer_set.load([int], x)
    assert obj == [10]
    obj = object_serializer_set.dump([int], obj)
    assert obj == [10]


def test_list_serializer_json_schema(object_serializer_set):
    schema = object_serializer_set.to_json_schema([str])
    assert schema == {"type": "array", "items": {"type": "string"}}


def test_object_serializer_set_can_handle(object_serializer_set):
    schema = object_serializer_set.to_json_schema([str])
    assert schema == {"type": "array", "items": {"type": "string"}}


@pytest.mark.parametrize(
    "cls,inp,out,expected_out",
    [(List[int], [1, 2], [1, 2], {"type": "array", "items": {"type": "integer"}})],
)
def test_serializer_values(object_serializer_set, cls, inp, out, expected_out):
    assert object_serializer_set.to_json_schema(cls) == expected_out
    assert object_serializer_set.load(cls, out) == inp
    assert object_serializer_set.dump(cls, inp) == out
