import inspect
from .compat import getfullargspec
from .signature import get_signature
from swagger_schema import (
    Operation, Responses, Response, JsonSchemaObject
)


TRANSMUTE_HTTP_METHOD_ATTRIBUTE = "transmute_http_methods"


class TransmuteFunction(object):
    """
    TransmuteFunctions wrap a function and add metadata,
    allowing transmute frameworks to extract that information for
    their own use (such as web handler generation or automatic
    documentation)
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
        self.description = func.__doc__ or ""
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
        self.swagger = self._get_swagger_operation()
        # this is to make discovery easier.
        # TODO: make sure this doesn't mess up GC, as it's
        # a cyclic reference.
        if inspect.ismethod(func):
            func.__func__.transmute_func = self
        else:
            func.transmute_func = self

    def __call__(self, *args, **kwargs):
        return self.raw_func(*args, **kwargs)

    def _get_swagger_operation(self):
        """ get the swagger_schema operation representation. """
        return Operation(
            summary=self.description,
            description=self.description,
            consumes=self.produces,
            produces=self.produces,
            responses=Responses({
                "200": Response(
                    description="success",
                    schema=JsonSchemaObject({
                        "properties": {
                            "success": {"type": "boolean"},
                            "result": {"type": "string"}
                        },
                        "required": ["success", "result"]
                    })
                ),
                "400": Response(
                    description="invalid input received",
                    schema=JsonSchemaObject({
                        "properties": {
                            "success": {"type": "boolean"},
                            "message": {"type": "string"}
                        },
                        "required": ["success", "message"]
                    })
                )
            })
        )
