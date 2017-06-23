from ..compat import all_string_types, string_type


class IntSerializer:

    def can_handle(self, cls):
        return issubclass(cls, int)

    @staticmethod
    def to_json_schema(cls):
        return {"type": "integer"}

    @staticmethod
    def load(cls, obj):
        return int(obj)

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
        return float(obj)

    @staticmethod
    def dump(cls, obj):
        return obj


class StringSerializer:

    def can_handle(self, cls):
        return any(
            issubclass(cls, t) for t in all_string_types
        )

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
        return obj

    @staticmethod
    def dump(cls, obj):
        return obj
