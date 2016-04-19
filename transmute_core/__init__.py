from .decorators import (
    PUT, POST, DELETE, annotate
)
from .schematics_serializer import SchematicsSerializer
from .contenttype_serializers import get_default_serializer_set
from .exceptions import APIException


class TransmuteContext(object):
    """
    TransmuteContext encapsulates all the configuration that transmute's
    core framework requires for all functionality it provides.

    When it's required to provide some customization on some
    of web-transmute's global values, a context can be used.

    In the case of multiple applications with
    """

    def __init__(self, serializers=None, contenttype_serializers=None):
        self._serializers = serializers or SchematicsSerializer()
        self._contenttype_serializers = (
            contenttype_serializers or
            get_default_serializer_set()
        )

    @property
    def serializers(self):
        return self._serializers

    @property
    def contenttype_serializers(self):
        return self._contenttype_serializers

# a global context is provided, if a singleton is sufficient
# or deviations from the defaults are unnescessary
default_context = TransmuteContext()
