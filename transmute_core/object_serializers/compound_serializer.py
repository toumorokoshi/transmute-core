class ListSerializer(object):
    """serializer for lists"""

    def __init__(self, subtype_serializer):
        self._subtype_serializer = subtype_serializer

    def can_handle(self, cls):
        if isinstance(cls, list):
            return True

    def to_json_schema(self, cls):
        subtype = cls[0]
        subtype_serializer = self._subtype_serializer[subtype]
        subtype_schema = subtype_serializer.to_json_schema(subtype)
        return {"type": "array", "items": subtype_schema}

    def dump(self, cls, value):
        subtype = cls[0]
        serializer = self._subtype_serializer[subtype]
        return [serializer.dump(subtype, el) for el in value]

    def load(self, cls, value):
        subtype = cls[0]
        serializer = self._subtype_serializer[subtype]
        return [serializer.load(subtype, el) for el in value]
