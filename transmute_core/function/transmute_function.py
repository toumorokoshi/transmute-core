import inspect
from swagger_schema import (
    Operation, Responses, Response, JsonSchemaObject, Path
)
from ..compat import getfullargspec
from ..context import default_context
from .attributes import TransmuteAttributes
from .signature import FunctionSignature
from .parameters import get_parameters
from ..exceptions import InvalidTransmuteDefinition


class TransmuteFunction(object):
    """
    TransmuteFunctions wrap a function and add metadata,
    allowing transmute frameworks to extract that information for
    their own use (such as web handler generation or automatic
    documentation)
    """

    params = ["error_exceptions"]

    def __init__(self, func, args_not_from_request=None):
        """
        :param list(str) args_not_from_request: a list of arguments that
            transmute_function should not retrieve from the request
            (e.g. from query parameters). This is useful for frameworks
            with pass in an argument to represent the request, or response object.
        """
        # arguments should be the arguments passed into
        # the function
        #
        # the return type should be specified. If nothing is
        # passed in, a NoneType is returned.
        # for a dynamic language like Python, it's not a huge deal:
        # transmute will still json serialize whatever object you pass it.
        # however, the return type is valuable for autodocumentation systems.
        attrs = getattr(func, "transmute", TransmuteAttributes())
        self._validate_attributes(attrs)
        # these are the paths that the transmute function
        # should respond to.
        self.paths = attrs.paths
        argspec = getfullargspec(func)
        self.signature = FunctionSignature.from_argspec(argspec)
        self.return_type = argspec.annotations.get("return")
        self.parameters = get_parameters(
            self.signature, attrs, arguments_to_ignore=args_not_from_request
        )
        # description should be a description of the api
        # endpoint, for use in autodocumentation
        self.description = func.__doc__ or ""
        # error_exceptions represents the exceptions
        # that should be caught and return an API exception
        self.error_exceptions = tuple(attrs.error_exceptions)
        # these are the http methods that should route to the given function.
        self.methods = attrs.methods
        self.raw_func = func
        # this is to make discovery easier.
        # TODO: make sure this doesn't mess up GC, as it's
        # a cyclic reference.
        if inspect.ismethod(func):
            func.__func__.transmute_func = self
        else:
            func.transmute_func = self

    def __call__(self, *args, **kwargs):
        return self.raw_func(*args, **kwargs)

    def get_swagger_path(self, context=default_context):
        operation = self.get_swagger_operation(context)
        path = Path()
        for m in self.methods:
            setattr(path, m.lower(), operation)
        return path

    def get_swagger_operation(self, context=default_context):
        """
        get the swagger_schema operation representation.
        """
        consumes = produces = context.contenttype_serializers.keys()
        return Operation(
            summary=self.description,
            description=self.description,
            consumes=consumes,
            produces=produces,
            responses=Responses({
                "200": Response(
                    description="success",
                    schema=JsonSchemaObject({
                        "properties": {
                            "success": {"type": "boolean"},
                            "result": context.serializers.to_json_schema(
                                self.return_type
                            )
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

    @staticmethod
    def _validate_attributes(attrs):
        """
        validate a TransmuteAttributes contains valid configuration
        that can be converted into a TransmuteFunction.
        """
        if len(attrs.paths) == 0:
            raise InvalidTransmuteDefinition(
                "at least one path is required for a valid set of transmute attribute: {0}".format(str(attrs))
            )
