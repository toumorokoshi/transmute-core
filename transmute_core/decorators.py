from .compat import string_type
from .function import (
    TRANSMUTE_HTTP_METHOD_ATTRIBUTE,
    TRANSMUTE_BODY_PARAMETERS,
    TRANSMUTE_QUERY_PARAMETERS
)


def describe(methods=None, query_parameters=None, body_parameters=None):
    """
    describe allows function annotations
    """
    # if we have a single method, make it a list.
    if isinstance(methods, string_type):
        methods = [methods]

    key_map = {
        TRANSMUTE_HTTP_METHOD_ATTRIBUTE: methods,
        TRANSMUTE_QUERY_PARAMETERS: query_parameters,
        TRANSMUTE_BODY_PARAMETERS: query_parameters
    }

    def decorator(f):
        for key, value in key_map.items():
            if value is not None:
                setattr(f, key, value)
        return f
    return decorator


def annotate(annotations):
    """
    in python2, native annotions on parameters do not exist:
    def foo(a : str, b: int) -> bool:
        ...

    this provides a way to provide attribute annotations:

    @annotate({"a": str, "b": int, "return": bool})
    def foo(a, b):
        ...
    """

    def decorate(func):
        func.__annotations__ = annotations
        return func

    return decorate
