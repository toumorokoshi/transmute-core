from transmute_core.exceptions import WebTransmuteException


class NoSerializerFound(WebTransmuteException):
    """
    raised when a serializer does not exist to handle the
    desired content type.
    """


class SerializerSet(object):
    """
    composes multiple serializers, delegating commands to one
    that can handle the desired content type.
    """

    def __init__(self, serializer_list):
        self._serializers = serializer_list

    def to_type(self, content_type, data):
        serializer = self.get_serializer_for_type(content_type)
        return serializer.to_type(data)

    def from_type(self, content_type, raw_bytes):
        serializer = self.get_serializer_for_type(content_type)
        return serializer.from_type(raw_bytes)

    def get_serializer_for_type(self, content_type):
        for serializer in self._serializers:
            if serializer.can_handle(content_type):
                return serializer
        raise NoSerializerFound(
            "unable to find serializer for " + content_type + "in: " +
            str(self._serializers)
        )
