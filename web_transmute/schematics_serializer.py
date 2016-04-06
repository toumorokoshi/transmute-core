from schematics.types import (
    BooleanType,
    IntType,
    FloatType,
    DecimalType,
    StringType
)
from schematics.exceptions import ConversionError
from .exceptions import SerializationException
from decimal import Decimal
from .compat import string_type

MODEL_MAP = {
    int: IntType(),
    bool: BooleanType(),
    float: FloatType(),
    Decimal: DecimalType(),
    string_type: StringType(),
}


class SchematicsSerializer(object):

    def __init__(self, builtin_models=None):
        builtin_models = builtin_models or MODEL_MAP
        self._models = dict(builtin_models)

    def load(self, model, value):
        try:
            if model in self._models:
                return self._models[model].to_native(value)
            return model(value)
        except ConversionError as e:
            raise SerializationException(str(e))

    def dump(self, model, value):
        try:
            if model in self._models:
                return self._models[model].to_primitive(value)
            return model.to_primitive(value)
        except ConversionError as e:
            raise SerializationException(str(e))
