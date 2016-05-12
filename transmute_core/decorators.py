from .compat import string_type
from .function import (
    TRANSMUTE_HTTP_METHOD_ATTRIBUTE,
    TRANSMUTE_BODY_PARAMETERS,
    TRANSMUTE_QUERY_PARAMETERS
)


def describe(methods=None, query_parameters=None, body_parameters=None):
    """describe is a decorator to customize the rest API
    that transmute generates, such as choosing
    certain arguments to be query parameters or
    body parameters, or a different method.

    :param list(str) methods: the methods this function should respond to. if non is set, transmute defaults to a GET.

    :param list(str) query_parameters: the names of arguments that should be query parameters

    :param list(str) body_parameters: the names of arguments that should be body parameters
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

    .. code-block:: python

        def foo(a : str, b: int) -> bool:
            ...

    this provides a way to provide attribute annotations:

    .. code-block:: python

        @annotate({"a": str, "b": int, "return": bool})
        def foo(a, b):
            ...
    """

    def decorate(func):
        func.__annotations__ = annotations
        return func

    return decorate
