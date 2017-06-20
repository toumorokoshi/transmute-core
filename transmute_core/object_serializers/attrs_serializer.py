from .interface import ObjectSerializer
from cattr import structure, unstructure
from ..exceptions import SerializationException
from cattr.vendor.typing import (
    Optional,
    List, MutableSequence, Sequence,
    Tuple,
    MutableSet, Set,
    FrozenSet,
    Dict, MutableMapping, Mapping,
    Union,
)
import attr


class AttrsSerializer(ObjectSerializer):
    """
    An ObjectSerializer which allows the serialization of
    basic types and attrs classes.
    """

    def __init__(self):
        pass

    def load(self, model, value):
        """
        Converts unstructured data into structured data, recursively.
        """
        try:
            res = structure(value, model)
        except Exception as e:
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
            res = unstructure(value)
        except Exception as e:
            raise SerializationException(str(e))
        return res


# Help Functions
# def _is_attr_class(cls):
#     try:
#         attrs = getattr(cls, "__attrs_attrs__", None)
#     except Exception:
#         return False
#     return attrs is not None
