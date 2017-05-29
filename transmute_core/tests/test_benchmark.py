import cProfile
import json
import pytest
import sys
from transmute_core import (
    TransmuteFunction, describe, annotate,
    ParamExtractor, NoArgument, process_result
)
from schematics.models import Model
from schematics.types import StringType, BooleanType, IntType
from schematics.types.compound import ModelType


class User(Model):
    name = StringType()
    age = IntType()


class ComplexModel(Model):
    user = ModelType(User)
    description = StringType()
    is_allowed = BooleanType()


@describe(paths="/foo", body_parameters="body")
@annotate({"body": ComplexModel, "return": ComplexModel})
def complex_body_method(body):
    return body


@describe(paths="/foo", body_parameters="body")
@annotate({"body": int, "return": int})
def simple_body_method(body):
    return body


def execute(context, func, obj_as_json):
    extractor = ParamExtractorMock(obj_as_json)
    args, kwargs = extractor.extract_params(
        context, func, "application/json"
    )
    exc, result = None, None
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        exc = e
        exc.__traceback__ = sys.exc_info[:2]
    process_result(func, context, result, exc, "application/json")


def test_complex_benchmark(benchmark, context):
    """
    a benchmark of a fake full execution flow of a transmute function.
    """
    obj = ComplexModel({
        "user": {
            "name": "Richard Stallman",
            "age": 104
        },
        "description": "this is a test",
        "is_allowed": True
    })

    complex_func = TransmuteFunction(complex_body_method)
    complex_json = json.dumps(obj.to_primitive())

    benchmark(lambda: execute(context, complex_func, complex_json))


def test_simple_benchmark(benchmark, context):

    simple_func = TransmuteFunction(simple_body_method)
    simple_json = json.dumps(1)

    benchmark(lambda: execute(context, simple_func, simple_json))

    # def profile():
    #     for i in range(10000):
    #         execute()
    # cProfile.runctx('profile()', globals(), locals())


class ParamExtractorMock(ParamExtractor):

    def __init__(self, body):
        self._body = body

    @property
    def body(self):
        return self._body

    def _get_framework_args(self):
        return {}

    def _query_argument(self, key, is_list):
        return NoArgument

    def _header_argument(self, key):
        return NoArgument

    def _path_argument(self, key):
        return NoArgument
