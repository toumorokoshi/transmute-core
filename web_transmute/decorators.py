from .function import TRANSMUTE_HTTP_METHOD_ATTRIBUTE


def PUT(f):
    """
    this labels a function as one that updates data.
    """
    _add_http_method_to_func("PUT", f)
    return f


def POST(f):
    """
    this labels a function as one that creates data.
    """
    _add_http_method_to_func("POST", f)
    return f


def DELETE(f):
    """
    this labels a function as one that deletes data.
    """
    _add_http_method_to_func("DELETE", f)
    return f


def _add_http_method_to_func(http_method, func):
    if not hasattr(func, TRANSMUTE_HTTP_METHOD_ATTRIBUTE):
        setattr(func, TRANSMUTE_HTTP_METHOD_ATTRIBUTE, set())
    getattr(func, TRANSMUTE_HTTP_METHOD_ATTRIBUTE).add(http_method)


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
