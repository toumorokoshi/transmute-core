import sys
from transmute_core import process_result, ParamExtractor


class ParamExtractorMock(ParamExtractor):
    def __init__(self, body):
        self._body = body

    @property
    def body(self):
        return self._body

    def _get_framework_args(self):
        return {}

        return NoArgument

    def _header_argument(self, key):
        return NoArgument

    def _path_argument(self, key):
        return NoArgument


def execute(context, func, obj_as_json):
    extractor = ParamExtractorMock(obj_as_json)
    args, kwargs = extractor.extract_params(context, func, "application/json")
    exc, result = None, None
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        exc = e
        exc.__traceback__ = sys.exc_info[:2]
    process_result(func, context, result, exc, "application/json")
