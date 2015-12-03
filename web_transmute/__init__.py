from .decorators import (
    PUT, POST, DELETE, annotate
)

from .serializer_cache import SerializerCache

# for most cases, a global serializer cache is sufficient, so one is provided.
serializers = SerializerCache()
