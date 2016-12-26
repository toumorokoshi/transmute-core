from transmute_core.exceptions import NoSerializerFound


class SerializerSet(object):
    """
    composes multiple serializers, delegating commands to one
    that can handle the desired content type.

    SerializerSet implements a dict-like interface. Retrieving
    serializers is done by get the content type item:

    .. code-block:: python

        serializers["application/json"]
    """

    def __init__(self, serializer_list):
        self.serializers = serializer_list
        assert len(self.serializers) > 0, "at least one serializer should be passed!"

    def _get_serializer_for_type(self, content_type):
        for serializer in self.serializers:
            if serializer.can_handle(content_type):
                return serializer
        raise NoSerializerFound(
            "unable to find serializer for " + content_type + "in: " +
            str(self.serializers)
        )

    def __getitem__(self, content_type):
        """
        from a given content type, returns the appropriate serializer.

        the list of serializers are interated, from first added to last,
        and returns the one who's can_handle returns true.
        """
        return self._get_serializer_for_type(content_type)

    def keys(self):
        """
        return a list of the contetn types this set supports.

        this is not a complete list: serializers can accept more than
        one content type. However, it is a good representation of the
        class of content types supported.
        """
        return_value = []
        for s in self.serializers:
            return_value += s.content_type
        return return_value

    @property
    def default(self):
        return self.serializers[0]
