import inspect
from swagger_schema import (
    Operation, Response, Schema, PathItem
)
from ..compat import getfullargspec
from ..context import default_context
from .attributes import TransmuteAttributes
from .signature import FunctionSignature
from .parameters import get_parameters
from ..swagger.function import get_swagger_parameters
from ..exceptions import (
    InvalidTransmuteDefinition,
)
from ..handler import process_result


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
        self.success_code = attrs.success_code
        argspec = getfullargspec(func)
        self.signature = FunctionSignature.from_argspec(argspec)
        self.response_types = self._parse_response_types(argspec, attrs)
        self.parameters = get_parameters(
            self.signature, attrs, arguments_to_ignore=args_not_from_request
        )
        # description should be a description of the api
        # endpoint, for use in autodocumentation
        self.description = inspect.cleandoc(func.__doc__ or "")
        # summary should be a shortened version of description.
        self.summary = self._summary(self.description)
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

    def get_response_by_code(self, code):
        """ return the return type, by code """
        return self.response_types.get(code, {}).get("type")

    def get_swagger_path(self, context=default_context):
        operation = self.get_swagger_operation(context)
        path = PathItem()
        for m in self.methods:
            setattr(path, m.lower(), operation)
        return path

    def get_swagger_operation(self, context=default_context):
        """
        get the swagger_schema operation representation.
        """
        consumes = produces = context.contenttype_serializers.keys()
        parameters = get_swagger_parameters(self.parameters, context)
        responses = {
            "400": Response({
                "description": "invalid input received",
                "schema": Schema({
                    "title": "FailureObject",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "result": {"type": "string"}
                    },
                    "required": ["success", "result"]
                })
            })
        }
        for code, details in self.response_types.items():
            responses[str(code)] = Response({
                "description": details.get("description"),
                "schema": context.response_shape.swagger(
                    context.serializers.to_json_schema(details["type"])
                )
            })
        return Operation({
            "summary": self.summary,
            "description": self.description,
            "consumes": consumes,
            "produces": produces,
            "parameters": parameters,
            "responses": responses,
            "operationId": self.raw_func.__name__
        })

    def process_result(self, context, result_body, exc, content_type):
        """
        given an result body and an exception object,
        return the appropriate result object,
        or raise an exception.
        """
        return process_result(
            self, context,
            result_body, exc, content_type
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

    @staticmethod
    def _parse_response_types(argspec, attrs):
        """
        from the given parameters, return back the response type dictionaries.
        """
        return_type = argspec.annotations.get("return") or None
        response_types = attrs.response_types.copy()
        if return_type or len(response_types) == 0:
            response_types[attrs.success_code] = {
                "type": return_type,
                "description": "success"
            }
        return response_types

    @staticmethod
    def _summary(description):
        for s in description.splitlines():
            if s != "":
                return s
        return ""
