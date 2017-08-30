from ..interface import ObjectSerializer
from jsonschema_extractor import init_default_extractor
from .converter import create_cattrs_converter
from ...exceptions import SerializationException


class CattrsSerializer(ObjectSerializer):
    """
    A serializer that's intended to become
    the pattern for 2.0
    """
    def __init__(self):
        self._schema_extractor = init_default_extractor()
        self._cattrs_converter = create_cattrs_converter()

    def can_handle(self, cls):
        """
        this will theoretically be compatible with everything
        """
        return True

    def load(self, model, value):
        try:
            return self._cattrs_converter.structure(value, model)
        except ValueError as e:
            raise SerializationException(str(e))


    def dump(self, model, value):
        try:
            return self._cattrs_converter.unstructure(value)
        except ValueError as e:
            raise SerializationException(str(e))

    def to_json_schema(self, model):
        return self._schema_extractor.extract(model)
