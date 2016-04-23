from transmute_core.exceptions import NoSerializerFound


class SerializerSet(object):
    """
    composes multiple serializers, delegating commands to one
    that can handle the desired content type.
    """

    def __init__(self, serializer_list):
        self._serializers = serializer_list

    def _get_serializer_for_type(self, content_type):
        for serializer in self._serializers:
            if serializer.can_handle(content_type):
                return serializer
        raise NoSerializerFound(
            "unable to find serializer for " + content_type + "in: " +
            str(self._serializers)
        )

    def __getitem__(self, content_type):
        return self._get_serializer_for_type(content_type)
