from marshmallow import fields
from .compat import string_type


def get_default_serializers():
    return {
        int: fields.Integer(),
        bool: fields.Boolean(),
        float: fields.Float(),
        string_type: fields.String()
    }


class SerializerCache(object):

    def __init__(self, cache=None):
        self._cache = cache or get_default_serializers()

    def __getitem__(self, typ):
        if typ not in self._cache:
            self._cache[typ] = typ.transmute_serializer
        return self._cache[typ]

    def __setitem__(self, typ, serializer):
        self._cache[typ] = serializer
