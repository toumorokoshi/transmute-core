import attr
import cProfile
import attr
import json
import pytest
import sys
from attr.validators import instance_of
from transmute_core import (
    TransmuteFunction,
    describe,
    annotate,
    ParamExtractor,
    NoArgument,
)
from schematics.models import Model
from schematics.types import StringType, BooleanType, IntType
from schematics.types.compound import ModelType
from .utils import execute


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


@describe(paths="/foo", body_parameters="body")
@annotate({"body": str, "return": str})
def body_string(body):
    return body


def test_large_str_benchmark(benchmark, context):
    """
    a benchmark of a fake full execution flow of a transmute function.
    """
    s = "a" * 100000

    func = TransmuteFunction(body_string)
    obj_json = json.dumps(s)

    benchmark(lambda: execute(context, func, obj_json))


def test_complex_benchmark(benchmark, context):
    """
    a benchmark of a fake full execution flow of a transmute function.
    """
    obj = ComplexModel(
        {
            "user": {"name": "Richard Stallman", "age": 104},
            "description": "this is a test",
            "is_allowed": True,
        }
    )

    complex_func = TransmuteFunction(complex_body_method)
    complex_json = json.dumps(context.serializers.dump(type(obj), obj))

    benchmark(lambda: execute(context, complex_func, complex_json))


def test_simple_benchmark(benchmark, context):

    simple_func = TransmuteFunction(simple_body_method)
    simple_json = json.dumps(1)

    benchmark(lambda: execute(context, simple_func, simple_json))
