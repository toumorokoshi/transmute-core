from .function.signature import NoDefault
from .exceptions import (
    APIException, NoSerializerFound
)
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

        args = {}
        framework_args = self._get_framework_args()
        for key, value in framework_args.items():
            if signature.get_argument(key):
                args[key] = value

        empty_args = []

        for name, arginfo in parameters.query.items():
            if name in framework_args:
                continue
            values = self._query_argument(
                name, isinstance(arginfo.type, list)
            )
            if values is NoArgument:
                empty_args.append(arginfo)
            else:
                args[name] = context.serializers.load(arginfo.type, values)

        for name, arginfo in parameters.header.items():
            if name in framework_args:
                continue
            value = self._header_argument(name)
            if value is NoArgument:
                empty_args.append(arginfo)
            else:
                args[name] = context.serializers.load(arginfo.type, value)

        if len(parameters.body) > 0:
            try:
                serializer = context.contenttype_serializers[content_type]
            except NoSerializerFound:
                raise APIException("unable to extract parameters for content type {0}. Supported types are: {1}".format(
                    content_type, context.contenttype_serializers.keys()
            ))
            if not self.body:
                body_dict = {}
            else:
                body_dict = serializer.load(self.body)
            for name, arginfo in parameters.body.items():
                if name in framework_args:
                    continue
                if name in body_dict:
                    args[name] = context.serializers.load(arginfo.type, body_dict[name])
                else:
                    empty_args.append(arginfo)

        for name, arginfo in parameters.path.items():
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

        pos_args = []
        for arg in signature.args:
            pos_args.append(args[arg.name])
            del args[arg.name]
        return pos_args, args

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
        """ return the request body. """
        raise NotImplementedError()

    def _query_argument(self, key, is_list):
        raise NotImplementedError()

    def _header_argument(self, key):
        raise NotImplementedError()

    def _path_argument(self, key):
        raise NotImplementedError()
