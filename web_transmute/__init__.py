from .decorators import (
    PUT, POST, DELETE, annotate
)
from .schematics_serializer import SchematicsSerializer
from .contenttype_serializers import get_default_serializer_set

# for most cases, a global serializer cache is sufficient, so one is provided.
serializers = SchematicsSerializer()
contenttype_serializers = get_default_serializer_set()
