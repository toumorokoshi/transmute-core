from .interface import ObjectSerializer
import attr
import cattr
import attrs_jsonschema
from ..exceptions import SerializationException


class AttrsSerializer(ObjectSerializer):
    """
    An ObjectSerializer which allows the serialization of
    basic types and attrs classes.
    """

    def can_handle(self, cls):
        try:
            attr.fields(cls)
            return True
        except:
            return False

    def load(self, model, value):
        """
        Converts unstructured data into structured data, recursively.
        """
        try:
            res = cattr.structure(value, model)
        except (ValueError, TypeError) as e:
            raise SerializationException(str(e))
        return res

    def dump(self, model, value):
        """
        Convert attrs data into unstructured data with basic types, recursively:

        - attrs classes => dictionaries
        - Enumeration => values
        - Other types are let through without conversion,
          such as, int, boolean, dict, other classes.
        """
        try:
            res = cattr.unstructure(value)
        except (ValueError, TypeError) as e:
            raise SerializationException(str(e))
        return res

    def to_json_schema(self, cls):
        return attrs_jsonschema.extract(cls)
