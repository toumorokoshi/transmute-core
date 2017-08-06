from .schematics_serializer import SchematicsSerializer
from .compound_serializer import (
    ListSerializer
)
from .interface import ObjectSerializer
from .serializer_set import ObjectSerializerSet
from .primitive_serializer import (
    BoolSerializer,
    FloatSerializer,
    NoneSerializer,
    IntSerializer,
    StringSerializer
)


def get_default_object_serializer_set():
    s = ObjectSerializerSet([
        BoolSerializer(),
        FloatSerializer(),
        NoneSerializer(),
        IntSerializer(),
        StringSerializer(),
        SchematicsSerializer()
    ])
    s.serializers.append(ListSerializer(s))
    return s
