from .interface import ObjectSerializer
from collections import OrderedDict
from schematics.types import (
    BaseType,
    BooleanType,
    DecimalType,
    FloatType,
    IntType,
    NumberType,
    StringType
)
from schematics.models import Model, ModelMeta
from schematics.types.compound import (
    CompoundType, ListType, ModelType, DictType
)
from schematics.exceptions import BaseError
from schematics.transforms import get_import_context
from ..exceptions import SerializationException
from decimal import Decimal
from ..compat import all_string_types

MODEL_MAP = {
    int: IntType(),
    bool: BooleanType(),
    float: FloatType(),
    Decimal: DecimalType(),
    None: BaseType()
}

for t in all_string_types:
    MODEL_MAP[t] = StringType()


JSON_SCHEMA_MAP = OrderedDict([
    (BooleanType, {"type": "boolean"}),
    (NumberType, {"type": "number"}),
    (BaseType, {"type": "string"}),
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

    def __init__(self, builtin_models=None):
        builtin_models = builtin_models or MODEL_MAP
        self._models = dict(builtin_models)

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
        try:
            model = self._translate_to_model(model)
            result = model(value, context=get_import_context(
                oo=True
            ))
            if hasattr(result, "validate"):
                result.validate()
            return result
        except BaseError as e:
            raise SerializationException(str(e))

    def dump(self, model, value):
        try:
            model = self._translate_to_model(model)
            return model.to_primitive(value)
        except BaseError as e:
            raise SerializationException(str(e))

    def to_json_schema(self, model):
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
