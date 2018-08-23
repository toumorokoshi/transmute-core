from transmute_core.exceptions import NoSerializerFound


class ObjectSerializerSet(object):
    """
    composes multiple serializers, delegating commands to one
    that can handle the desired content type.

    SerializerSet implements a dict-like interface. Retrieving
    serializers is done by get the content type item:

    .. code-block:: python

        serializers["application/json"]
    """

    def __init__(self, serializer_list):
        self.serializers = list(serializer_list)
        self._cache = {}
        assert len(self.serializers) > 0, "at least one serializer should be passed!"

    def _get_serializer_for_type(self, cls):
        cls_key = self._to_key(cls)
        if cls_key not in self._cache:
            for serializer in self.serializers:
                try:
                    if serializer.can_handle(cls):
                        self._cache[cls_key] = serializer
                        return serializer
                except:
                    pass
            raise NoSerializerFound(
                "unable to find serializer for "
                + str(cls)
                + " in: "
                + str(self.serializers)
            )
        return self._cache[cls_key]

    def __getitem__(self, cls):
        """
        from a given content type, returns the appropriate serializer.

        the list of serializers are interated, from first added to last,
        and returns the one who's can_handle returns true.
        """
        return self._get_serializer_for_type(cls)

    def to_json_schema(self, cls):
        return self[cls].to_json_schema(cls)

    def dump(self, cls, value):
        return self[cls].dump(cls, value)

    def load(self, cls, value):
        return self[cls].load(cls, value)

    @staticmethod
    def _to_key(target_cls):
        if isinstance(target_cls, list):
            return tuple(target_cls)
        return target_cls
