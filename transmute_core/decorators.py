from .compat import string_type
from .function import TransmuteAttributes


def describe(**kwargs):
    """ describe is a decorator to customize the rest API
    that transmute generates, such as choosing
    certain arguments to be query parameters or
    body parameters, or a different method.

    :param list(str) paths: the path(s) for the handler to represent (using swagger's syntax for a path)

    :param list(str) methods: the methods this function should respond to. if non is set, transmute defaults to a GET.

    :param list(str) query_parameters: the names of arguments that
           should be query parameters. By default, all arguments are query_or path parameters for a GET request.

    :param list(str) body_parameters: the names of arguments that should be body parameters.
           By default, all arguments are either body or path parameters for a non-GET request.

    :param list(str) header_parameters: the arguments that should be passed into the header.

    :param list(str) path_parameters: the arguments that are specified by the path. By default, arguments
            that are found in the path are used first before the query_parameters and body_parameters.
    """
    # if we have a single method, make it a list.
    if isinstance(kwargs.get("paths"), string_type):
        kwargs["paths"] = [kwargs["paths"]]
    if isinstance(kwargs.get("methods"), string_type):
        kwargs["methods"] = [kwargs["methods"]]
    attrs = TransmuteAttributes(**kwargs)

    def decorator(f):
        if hasattr(f, "transmute"):
            f.transmute = f.transmute | attrs
        else:
            f.transmute = attrs
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
