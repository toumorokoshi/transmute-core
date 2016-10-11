import pytest
from transmute_core.contenttype_serializers.serializer_set import SerializerSet


def test_serializer_set_empty_list():
    with pytest.raises(AssertionError):
        SerializerSet([])
