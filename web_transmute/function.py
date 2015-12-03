import inspect
from .compat import getfullargspec
from .signature import get_signature


TRANSMUTE_HTTP_METHOD_ATTRIBUTE = "transmute_http_methods"


class NoDefault(object):

    def __str__(self):
        return "NoDefault"

    def __repr__(self):
        return "NoDefault"

NoDefault = NoDefault()


class TransmuteFunction(object):
    """
    VoodooFunctions are objects that wrap a method, allowing
    extensions to extract metadata for their own use (such as
    automatic documentation)
    """

    params = ["error_exceptions"]

    def __init__(self, func, error_exceptions=None):
        # arguments should be the arguments passed into
        # the function
        #
        # the return type should be specified. If nothing is
        # passed in, a NoneType is returned.
        # for a dynamic language like Python, it's not a huge deal:
        # transmute will still json serialize whatever object you pass it.
        # however, the return type is valuable for autodocumentation systems.
        self.argspec = getfullargspec(func)
        self.signature = get_signature(self.argspec)
        self.return_type = self.argspec.annotations.get("return")
        # description should be a description of the api
        # endpoint, for use in autodocumentation
        self.description = func.__doc__
        # error_exceptions represents the exceptions
        # that should be caught and return an API exception
        self.error_exceptions = error_exceptions
        # these are the http methods that should route to the given function.
        self.http_methods = getattr(
            func, TRANSMUTE_HTTP_METHOD_ATTRIBUTE, set(["GET"])
        )
        # produces represents the return types supported
        # by the final function
        self.produces = ["application/json"]
        self.raw_func = func
        # status_codes represents the possible status codes
        # the function can return
        self.responses = _get_responses(self.return_type)
        # this is to make discovery easier.
        # TODO: make sure this doesn't mess up GC, as it's
        # a cyclic reference.
        if inspect.ismethod(func):
            func.__func__.transmute_func = self
        else:
            func.transmute_func = self

    def __call__(self, *args, **kwargs):
        return self.raw_func(*args, **kwargs)


def _get_responses(return_type):
    return {
        200: {
            "description": "success",
            "return_type": {"properties": {"success": {"type": bool},
                                           "result": {"type": return_type}},
                            "required": ["success", "result"]}
        },
        400: {
            "description": "invalid input received",
            "return_type": {"properties": {"success": {"type": bool},
                                           "message": {"type": str}},
                            "required": ["success", "message"]}
        }
    }
