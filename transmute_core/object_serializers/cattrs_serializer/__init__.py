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
        # to be compatible with older versions of cattrs,
        # attempt to discover the version of structure_error to use.
        if hasattr(self._cattrs_converter, "_structure_error"):
            self._structure_error = self._cattrs_converter._structure_error
        else:
            self._structure_error = self._cattrs_converter._structure_default

    def can_handle(self, cls):
        """
        this will theoretically be compatible with everything,
        as cattrs can handle many basic types as well.
        """
        # cattrs uses a Singledispatch like function
        # under the hood.
        f = self._cattrs_converter._structure_func.dispatch(cls)
        return f != self._structure_error

    def load(self, model, value):
        """
        Converts unstructured data into structured data, recursively.
        """
        try:
            return self._cattrs_converter.structure(value, model)
        except (ValueError, TypeError) as e:
            raise SerializationException(str(e))

    def dump(self, model, value):
        """
        Convert attrs data into unstructured data with basic types, recursively:

        - attrs classes => dictionaries
        - Enumeration => values
        - Other types are let through without conversion,
          such as, int, boolean, dict, other classes.
        """
        try:
            return self._cattrs_converter.unstructure(value)
        except (ValueError, TypeError) as e:
            raise SerializationException(str(e))

    def to_json_schema(self, model):
        return self._schema_extractor.extract(model)
