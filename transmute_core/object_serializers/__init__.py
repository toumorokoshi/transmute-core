from .cattrs_serializer import CattrsSerializer
from .compound_serializer import ListSerializer
from .schematics_serializer import SchematicsSerializer
from .interface import ObjectSerializer
from .serializer_set import ObjectSerializerSet


def get_default_object_serializer_set():
    s = ObjectSerializerSet([
        SchematicsSerializer(),
        CattrsSerializer(),
    ])
    s.serializers.insert(0, ListSerializer(s))
    return s
