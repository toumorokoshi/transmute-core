import sys
from functools import wraps
from flask import request, Response
from transmute_core import ParamExtractor, NoArgument


def create_routes_and_handler(transmute_func, context):
    @wraps(transmute_func.raw_func)
    def handler(*args, **kwargs):
        exc, result = None, None
        try:
            args, kwargs = _param_instance.extract_params(
                context,
                transmute_func,
                request.content_type,
            )
            result = transmute_func(*args, **kwargs)
        except Exception as e:
            exc = e
            exc.__traceback__ = sys.exc_info()[2]
        response = transmute_func.process_result(
            context, result, exc, request.content_type
        )
        return Response(
            response["body"],
            status=response["code"],
            mimetype=response["content-type"],
            headers=response["headers"],
        )

    return (_convert_paths_to_flask(transmute_func.paths), handler)


def _convert_paths_to_flask(transmute_paths):
    """flask has it's own route syntax, so we convert it."""
    paths = []
    for p in transmute_paths:
        paths.append(p.replace("{", "<").replace("}", ">"))
    return paths


class ParamExtractorFlask(ParamExtractor):
    def _get_framework_args(self):
        return {}

    @property
    def body(self):
        return request.get_data()

    @staticmethod
    def _query_argument(key, is_list):
        if key not in request.args:
            return NoArgument
        if is_list:
            return request.args.getlist(key)
        else:
            return request.args[key]

    @staticmethod
    def _header_argument(key):
        return request.headers.get(key, NoArgument)

    @staticmethod
    def _path_argument(key):
        return request.view_args.get(key, NoArgument)


_param_instance = ParamExtractorFlask()
