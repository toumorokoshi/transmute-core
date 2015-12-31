from .decorators import (
    PUT, POST, DELETE, annotate
)

from .serializer_cache import SerializerCache
from .contenttype_serializers import get_default_serializer_set

# for most cases, a global serializer cache is sufficient, so one is provided.
serializers = SerializerCache()
contenttype_serializers = get_default_serializer_set()
