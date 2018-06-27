from .interface import ObjectSerializer
from collections import OrderedDict
from datetime import datetime
from schematics.types import (
    BaseType,
    BooleanType,
    DecimalType,
    FloatType,
    IntType,
    NumberType,
    StringType,
    Serializable,
    DateTimeType,
    UUIDType,
    URLType
)
from schematics.models import ModelMeta, Model
from schematics.types.compound import (
    ListType, ModelType, DictType
)
from schematics.exceptions import BaseError, ConversionError
from schematics.transforms import get_import_context
from ..exceptions import SerializationException
from decimal import Decimal
from ..compat import all_string_types

JSON_SCHEMA_MAP = OrderedDict([
    (BooleanType, {"type": "boolean"}),
    (NumberType, {"type": "number"}),
    (UUIDType, {"type": "string", "format": "uuid"}),
    (URLType, {"type": "string", "format": "url"}),
    (StringType, {"type": "string"}),
    (DateTimeType, {"type": "string", "format": "date-time"}),
    (BaseType, {"type": "object"}),
])


class SchematicsSerializer(ObjectSerializer):
    """
    An ObjectSerializer which allows the serialization of
    basic types and schematics models.

    The valid types that SchematicsSerializer supports are:

    - int
    - float
    - bool
    - decimal
    - string
    - none
    - lists, in the form of [Type] (e.g. [str])
    - any type that extends the schematics.models.Model.
    """
    VALID_BASE_CLASSES = [BaseType, ModelMeta, Model, Serializable]

    def can_handle(self, cls):
        if cls in self._models:
            return True
        if any(isinstance(cls, t) for t in self.VALID_BASE_CLASSES):
             return True
        if not isinstance(cls, type):
            return False
        if any(issubclass(cls, t) for t in self.VALID_BASE_CLASSES):
            return True

    def __init__(self, builtin_models=None):
        self._models = {}

    def _translate_to_model(self, model):
        model = self._to_key(model)

        if isinstance(model, BaseType):
            return model

        if isinstance(model, ModelMeta):
            return ModelType(model)

        if model not in self._models and isinstance(model, tuple):
            self._models[model] = ListType(
                self._translate_to_model(model[0])
            )

        if model in self._models:
            return self._models[model]

        return model

    @staticmethod
    def _to_key(model):
        if isinstance(model, list):
            return tuple(model)
        return model

    def load(self, model, value):
        model = _enforce_instance(model)
        try:
            context = get_import_context(oo=True)
            model = self._translate_to_model(model)
            result = model(value, context=context)
            if isinstance(model, ModelType) or not isinstance(model, BaseType):
                result.validate()
            else:
                model.validate(result, context=context)
            return result
        except BaseError as e:
            raise SerializationException(str(e))
        except ConversionError as e:
            raise SerializationException(str(e))

    def dump(self, model, value):
        model = _enforce_instance(model)
        try:
            model = self._translate_to_model(model)
            return model.to_primitive(value)
        except BaseError as e:
            raise SerializationException(str(e))

    def to_json_schema(self, model):
        if isinstance(model, Serializable):
            model = model.type
        model = _enforce_instance(model)
        model = self._translate_to_model(model)
        return _to_json_schema(model)

_cache = {}


def _to_json_schema(model):
    if model not in _cache:
        _cache[model] = _to_json_schema_no_cache(model)
    return _cache[model]


def _to_json_schema_no_cache(model):
    if isinstance(model, ModelType):
        return _model_type_to_json_schema(model)
    elif isinstance(model, ListType):
        return _list_type_to_json_schema(model)
    elif isinstance(model, DictType):
        return _dict_type_to_json_schema(model)
    else:
        for cls, schema in JSON_SCHEMA_MAP.items():
            if isinstance(model, cls):
                return schema
    if isinstance(model, BaseType):
        return {"type": "object"}
    if isinstance(model, Serializable):
        return _to_json_schema_no_cache(model.type)
    raise SerializationException(
        "unable to create json schema for type " +
        "{0}. Expected a primitive or ".format(model) +
        " a schematics model or type"
    )


def _model_type_to_json_schema(model):
    required = []
    schema = {
        "title": model.model_name,
        "type": "object",
        "properties": {}
    }
    for name, field in model.fields.items():
        if field.required:
            required.append(name)
        schema["properties"][name] = _to_json_schema(field)
    if len(required) > 0:
        schema["required"] = required
    return schema


def _list_type_to_json_schema(list_type):
    return {
        "type": "array",
        "items": _to_json_schema(list_type.field)
    }


def _dict_type_to_json_schema(dict_type):
    return {
        "type": "object",
        "additionalProperties": _to_json_schema(dict_type.field)
    }


def _enforce_instance(model_or_class):
    """
    It's a common mistake to not initialize a
    schematics class. We should handle that by just
    calling the default constructor.
    """
    if (isinstance(model_or_class, type) and
        issubclass(model_or_class, BaseType)):
        return model_or_class()
    return model_or_class
