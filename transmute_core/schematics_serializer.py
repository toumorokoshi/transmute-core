from schematics.types import (
    BooleanType,
    IntType,
    FloatType,
    DecimalType,
    StringType
)
from schematics.types.compound import (
    ListType, ModelType
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

    def _translate_to_model(self, model):
        model = self._to_key(model)
        if model not in self._models and isinstance(model, tuple):
            self._models[model] = ListType(ModelType(model[0]))
        return model

    @staticmethod
    def _to_key(model):
        if isinstance(model, list):
            return tuple(model)
        return model

    def load(self, model, value):
        try:
            model = self._translate_to_model(model)
            if model in self._models:
                return self._models[model](value)
            return model(value)
        except ConversionError as e:
            raise SerializationException(str(e))

    def dump(self, model, value):
        try:
            model = self._translate_to_model(model)
            if model in self._models:
                return self._models[model].to_primitive(value)
            return model.to_primitive(value)
        except ConversionError as e:
            raise SerializationException(str(e))
