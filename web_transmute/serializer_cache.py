from marshmallow import fields
from marshmallow.exceptions import ValidationError
from .compat import string_type, with_metaclass


def get_default_serializers():
    return {
        int: Integer(),
        bool: Boolean(),
        float: Float(),
        string_type: String(),
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


class WithLoadDumpMeta(type):

    def __new__(cls, name, parents, dct):
        new_cls = super(WithLoadDumpMeta, cls).__new__(cls, name, parents, dct)
        new_cls.dump = new_cls.serialize
        new_cls.load = new_cls.deserialize
        return new_cls


class Integer(object):

    @staticmethod
    def load(data):
        try:
            return int(data)
        except ValueError as ve:
            raise ValidationError(str(ve))

    @staticmethod
    def dump(value):
        return value


class Boolean(object):

    @staticmethod
    def load(data):
        try:
            return str(data).lower().startswith("t")
        except ValueError as ve:
            raise ValidationError(str(ve))

    @staticmethod
    def dump(value):
        return value


class Float(object):

    @staticmethod
    def load(data):
        try:
            return float(data)
        except ValueError as ve:
            raise ValidationError(str(ve))

    @staticmethod
    def dump(value):
        return value


class String(object):

    @staticmethod
    def load(data):
        try:
            return str(data)
        except ValueError as ve:
            raise ValidationError(str(ve))

    @staticmethod
    def dump(value):
        return value
