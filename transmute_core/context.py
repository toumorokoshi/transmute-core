from .object_serializers import SchematicsSerializer
from .contenttype_serializers import get_default_serializer_set


class TransmuteContext(object):
    """
    TransmuteContext contains all of the configuration points for a
    framework based off of transmute.

    It is useful for customizing default behaviour in Transmute, such
    as serialization of additional content types, or using different
    serializers for objects to and from basic data times.
    """

    def __init__(self, serializers=None, contenttype_serializers=None):
        #:
        self.serializers = serializers or SchematicsSerializer()
        self.contenttype_serializers = (
            contenttype_serializers or
            get_default_serializer_set()
        )

# a global context is provided, if a singleton is sufficient
# or deviations from the defaults are unnescessary
default_context = TransmuteContext()
