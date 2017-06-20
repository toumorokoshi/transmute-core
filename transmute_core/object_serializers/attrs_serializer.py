from .interface import ObjectSerializer
import cattr
from ..exceptions import SerializationException


class AttrsSerializer(ObjectSerializer):
    """
    An ObjectSerializer which allows the serialization of
    basic types and attrs classes.
    """

    def load(self, model, value):
        """
        Converts unstructured data into structured data, recursively.
        """
        try:
            res = cattr.structure(value, model)
        except (ValueError, TypeError) as e:
            raise SerializationException(str(e))
        return res

    def dump(self, value):
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
