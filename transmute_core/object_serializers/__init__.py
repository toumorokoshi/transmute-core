from .compound_serializer import ListSerializer
from .cattrs_serializer import CattrsSerializer
from .schematics_serializer import SchematicsSerializer
from .interface import ObjectSerializer
from .serializer_set import ObjectSerializerSet
from .primitive_serializer import (
    NoneSerializer,
    IntSerializer,
    FloatSerializer,
    StringSerializer,
    BoolSerializer,
    DateTimeSerializer,
    DecimalSerializer,
)


DEFAULT_SERIALIZER_LIST = [
    SchematicsSerializer(),
    NoneSerializer(),
    BoolSerializer(),
    StringSerializer(),
    IntSerializer(),
    FloatSerializer(),
    DateTimeSerializer(),
    DecimalSerializer(),
    CattrsSerializer(),
]


def get_default_object_serializer_set():
    s = ObjectSerializerSet(DEFAULT_SERIALIZER_LIST)
    s.serializers.insert(0, ListSerializer(s))
    return s
