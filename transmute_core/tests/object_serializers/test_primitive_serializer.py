from ...object_serializers.primitive_serializer import BoolSerializer
import pytest


@pytest.mark.parametrize(
    "object, result",
    [
        ("true", True),
        ("false", False),
        ("some_other_str", False),
        ([], False),
        (["non-empty-list"], True),
        ({}, False),
        ({"non_empty_dict": "test_val"}, True),
    ],
)
def test_primitive_serializer_bool_serializer(object, result):
    serializer = BoolSerializer()
    assert BoolSerializer.load(serializer, object) == result
