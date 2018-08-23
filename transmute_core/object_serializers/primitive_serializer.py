from ..compat import all_string_types, string_type
from ..exceptions import SerializationException
from schematics.exceptions import BaseError
from schematics.types import DecimalType, DateTimeType
from decimal import Decimal
from datetime import datetime


class IntSerializer:
    def can_handle(self, cls):
        return issubclass(cls, int)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "integer"}

    @staticmethod
    def load(cls, obj):
        try:
            return int(obj)
        except ValueError as e:
            raise SerializationException(str(e))

    @staticmethod
    def dump(cls, obj):
        return obj


class FloatSerializer:
    def can_handle(self, cls):
        return issubclass(cls, float)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "number"}

    @staticmethod
    def load(cls, obj):
        try:
            return float(obj)
        except ValueError as e:
            raise SerializationException(str(e))

    @staticmethod
    def dump(cls, obj):
        return obj


class StringSerializer:
    def can_handle(self, cls):
        return any(issubclass(cls, t) for t in all_string_types)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "string"}

    @staticmethod
    def load(cls, obj):
        return obj

    @staticmethod
    def dump(cls, obj):
        return obj


class BoolSerializer:
    def can_handle(self, cls):
        return issubclass(cls, bool)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "boolean"}

    @staticmethod
    def load(cls, obj):
        if isinstance(obj, string_type):
            return obj.lower().startswith("t")
        return bool(obj)

    @staticmethod
    def dump(cls, obj):
        return obj


class NoneSerializer(object):
    def can_handle(self, cls):
        return cls is None

    @staticmethod
    def to_json_schema(cls):
        return {"type": "object"}

    @staticmethod
    def load(cls, obj):
        return obj

    @staticmethod
    def dump(cls, obj):
        return obj


class DecimalSerializer(object):

    SERIALIZER = DecimalType()

    def can_handle(self, cls):
        return issubclass(cls, Decimal)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "number"}

    def load(self, cls, obj):
        try:
            return self.SERIALIZER.to_native(obj)
        except BaseError as e:
            raise SerializationException(str(e))

    def dump(self, cls, obj):
        try:
            return self.SERIALIZER.to_primitive(obj)
        except BaseError as e:
            raise SerializationException(str(e))


class DateTimeSerializer(object):

    SERIALIZER = DateTimeType()

    def can_handle(self, cls):
        return issubclass(cls, datetime)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "string", "format": "date-time"}

    def load(self, cls, obj):
        try:
            return self.SERIALIZER.to_native(obj)
        except BaseError as e:
            raise SerializationException(str(e))

    def dump(self, cls, obj):
        try:
            return self.SERIALIZER.to_primitive(obj)
        except BaseError as e:
            raise SerializationException(str(e))
