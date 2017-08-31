import pytest
import sys

pytest.importorskip("cattr")

import attr
import cattr
import json
from attr.validators import instance_of
from transmute_core.exceptions import SerializationException
from typing import List
from cattr import typed
from transmute_core.object_serializers.cattrs_serializer import CattrsSerializer
from transmute_core import describe, annotate, TransmuteFunction
from .utils import execute

@pytest.fixture
def cattrs_serializer():
    return CattrsSerializer()

class Player(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score


@attr.s
class Card(object):
    name = typed(str, default="")
    price = typed(float, default=1.0)

@attr.s
class Hand(object):
    cards = typed(List[Card])


@attr.s
class Person(object):
    age = typed(int)
    bio = typed(str, default="")

    @age.validator
    def greater_than_zero(self, attribute, value):
        if value < 0:
            raise ValueError("must be greater than zero")
        return value


card_dict = {"name": "foo", "price": 10}
card = Card(**card_dict)
player = Player("kobe", 81)

@pytest.mark.parametrize("typ,inp,out", [
    (Card, card, card_dict),
    (List[Card], [card], [card_dict]),
    (Player, player, player)
])
def test_attrs_integration_dump(cattrs_serializer, typ, inp, out):
    assert cattrs_serializer.dump(typ, inp) == out


def test_attrs_integration_dump_exception(monkeypatch, cattrs_serializer):
    def mock_return(inp):
        raise ValueError("Random_Exception")
    monkeypatch.setattr(cattrs_serializer._cattrs_converter, "unstructure", mock_return)
    with pytest.raises(SerializationException):
        assert cattrs_serializer.dump(str, "random_str")


@pytest.mark.parametrize("typ,inp", [
    ([Card], [card_dict])
])
def test_attrs_integration_load_exception(cattrs_serializer, typ, inp):
    with pytest.raises(SerializationException):
        cattrs_serializer.load(typ, inp)


def test_attrs_validate_is_called(cattrs_serializer):
    with pytest.raises(SerializationException):
        cattrs_serializer.load(Person, {"age": -1, "bio": "foo"})


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    (List[Card], [card_dict], [card]),
])
def test_attrs_integration_load(cattrs_serializer, typ, inp, out):
    assert cattrs_serializer.load(typ, inp) == out


def test_to_json_schema(cattrs_serializer):
    assert cattrs_serializer.to_json_schema(Card) == {
        "type": "object",
        "title": "Card",
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"}
        },
        "required": []
    }

    assert cattrs_serializer.to_json_schema(Hand) == {
        "type": "object",
        "title": "Hand",
        "properties": {
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "title": "Card",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"}
                    },
                    "required": []
                }
            },
        },
        "required": ["cards"]
    }

@attr.s
class UserAttrs(object):
    name = attr.ib(validator=instance_of(str))
    age = attr.ib(validator=instance_of(int))


@attr.s
class UserAttrs(object):
    name = typed(str)
    age = typed(int)


@attr.s
class ComplexModelAttrs(object):
    user = typed(UserAttrs)
    description = typed(str)
    is_allowed = typed(bool)


@describe(paths="/foo", body_parameters="body")
@annotate({"body": ComplexModelAttrs, "return": ComplexModelAttrs})
def complex_body_method_attrs(body):
    return body


def test_complex_benchmark_attrs(benchmark, context):
    """
    a benchmark of a fake full execution flow of a transmute function.
    """
    obj = ComplexModelAttrs(
        user=UserAttrs(name="Richard Stallman", age=104),
        description="this is a test",
        is_allowed=True
    )

    complex_func = TransmuteFunction(complex_body_method_attrs)
    complex_json = json.dumps(context.serializers.dump(type(obj), obj))

    benchmark(lambda: execute(context, complex_func, complex_json))
