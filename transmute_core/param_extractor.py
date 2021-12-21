from .function.signature import NoDefault
from transmute_core.http_parameters import ParamSet, Param
from .exceptions import APIException, NoSerializerFound

NoArgument = object()


class ParamExtractor(object):
    """
    An abstract object to extend to handle
    extracting parameters from a request.
    """

    NoArgument = NoArgument

    def extract_params(self, context, transmute_func, content_type):
        parameters = transmute_func.parameters
        signature = transmute_func.signature
        content_type = content_type or context.contenttype_serializers.default.main_type

        args = {}
        framework_args = self._get_framework_args()
        for key, value in framework_args.items():
            if signature.get_argument(key):
                args[key] = value

        empty_args = []

        for name, param in parameters.query.items():
            arginfo = param.arginfo
            if name in framework_args:
                continue
            schema = context.serializers.to_json_schema(arginfo.type)
            is_list = "items" in schema
            values = self._query_argument(name, is_list)
            if values is NoArgument:
                empty_args.append(arginfo)
            else:
                if is_list and len(values) == 1:
                    values = values[0].split(",")
                args[name] = context.serializers.load(arginfo.type, values)

        for name, param in parameters.header.items():
            arginfo = param.arginfo
            if name in framework_args:
                continue
            value = self._header_argument(name)
            if value is NoArgument:
                empty_args.append(arginfo)
            else:
                args[name] = context.serializers.load(arginfo.type, value)

        if isinstance(parameters.body, Param) or len(parameters.body) > 0:
            try:
                serializer = context.contenttype_serializers[content_type]
            except NoSerializerFound:
                raise APIException(
                    "unable to extract parameters for content type {0}. Supported types are: {1}".format(
                        content_type, context.contenttype_serializers.keys()
                    )
                )
            if not self.body:
                body_dict = {}
            else:
                body_dict = serializer.load(self.body)

            if isinstance(parameters.body, Param):
                arginfo = parameters.body.arginfo
                args[arginfo.name] = context.serializers.load(arginfo.type, body_dict)
            else:
                for name, param in parameters.body.items():
                    arginfo = param.arginfo
                    if name in framework_args:
                        continue
                    if name in body_dict:
                        args[name] = context.serializers.load(
                            arginfo.type, body_dict[name]
                        )
                    else:
                        empty_args.append(arginfo)

        for name, param in parameters.path.items():
            arginfo = param.arginfo
            if name in framework_args:
                continue
            values = self._path_argument(name)
            if values is not NoArgument:
                args[name] = context.serializers.load(arginfo.type, values)
            else:
                empty_args.append(arginfo)

        required_params_not_passed = []

        for arg in empty_args:
            if arg.default is NoDefault:
                required_params_not_passed.append(arg.name)
            else:
                args[arg.name] = arg.default

        if len(required_params_not_passed) > 0:
            raise APIException(
                "required arguments {0} not passed".format(required_params_not_passed)
            )

        return signature.split_args(args)

    def _get_framework_args(self):
        """
        often, a framework provides specific variables that are passed
        into the handler function (e.g. the request object in
        aiohttp). return a dictionary of these arguments, which will be
        added to the function arguments if they appear.
        """
        pass

    @property
    def body(self):
        """return the request body."""
        raise NotImplementedError()

    def _query_argument(self, key, is_list):
        raise NotImplementedError()

    def _header_argument(self, key):
        raise NotImplementedError()

    def _path_argument(self, key):
        raise NotImplementedError()


def _fold(param_or_param_set, value_dict, request_context):
    # a single parameter consumes the whole dict
    if isinstance(param_or_param_set, Param):
        arginfo = param_or_param_set.arginfo
        value = request_context.context.serializers.load(arginfo.type, value_dict)
        request_context.args[argument.name] = value
    # a param set consumes the dict piece by piece
    else:
        for name, param in param_or_param_set.values():
            arginfo = param.arginfo
            if name in request_context.framework_args:
                continue
            if name in value_dict:
                value = context.serializers.load(arginfo.type, value_dict[name])
                request_context.args[arginfo.name] = value
            elif arginfo.default is not NoDefault:
                request_context.args[arginfo.name] = arginfo.default
            else:
                request_context.empty_args.append(name)
