import sys
import tornado.gen
from functools import wraps
from transmute_core import (
    ParamExtractor,
    NoArgument,
    default_context,
    TransmuteFunction,
)


def convert_to_handler(context=default_context):
    def decorator(fn):
        func = tornado.gen.coroutine(fn)
        transmute_func = TransmuteFunction(fn)

        @tornado.gen.coroutine
        @wraps(transmute_func.raw_func)
        def wrapper(self, *passed_args, **kwargs):
            result, exc = None, None
            content_type = self.request.headers.get("Content-Type", None)
            param_extractor = ParamExtractorTornado(self, kwargs)
            try:
                args, kwargs = param_extractor.extract_params(
                    context, transmute_func, content_type
                )
                args = list(passed_args) + args
                result = yield func(self, *args, **kwargs)
            except Exception as e:
                exc = e
                exc.__traceback__ = sys.exc_info()[2]
            response = transmute_func.process_result(context, result, exc, content_type)
            self.set_header("Content-Type", response["content-type"])
            self.set_status(response["code"])
            self.finish(response["body"])

        wrapper.transmute_func = transmute_func
        return wrapper

    return decorator


class ParamExtractorTornado(ParamExtractor):
    def __init__(self, handler_self, path_kwargs):
        self._handler_self = handler_self
        self._request = handler_self.request
        self._path_kwargs = path_kwargs

    @property
    def body(self):
        return self._request.body

    def _query_argument(self, key, is_list):
        qa = self._request.query_arguments
        if key not in qa:
            return NoArgument
        if is_list:
            return [v.decode() for v in qa[key]]
        else:
            return qa[key][0].decode()

    def _header_argument(self, key):
        return self._request.headers.get(key, NoArgument)

    def _path_argument(self, key):
        return self._path_kwargs.get(key, NoArgument)

    def _get_framework_args(self):
        return {}
