import uuid
import pytest
from datetime import datetime
from schematics.models import Model
from schematics.types import StringType, IntType, BaseType, UUIDType, URLType, Serializable
from schematics.types.compound import DictType, ModelType
from schematics.exceptions import ValidationError
from transmute_core.exceptions import SerializationException


class Card(Model):
    name = StringType()
    price = IntType()


def greater_than_zero(value):
    if value < 0:
        raise ValidationError("must be greater than zero")
    return value


class Person(Model):
    age = IntType(required=True, validators=[greater_than_zero])
    bio = StringType()

card_dict = {"name": "foo", "price": 10}
card = Card(card_dict)


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card, card_dict),
    ([Card], [card], [card_dict])
])
def test_schematics_integration_dump(serializer, typ, inp, out):
    assert serializer.dump(typ, inp) == out


def test_schematics_validate_is_called(serializer):
    with pytest.raises(SerializationException):
        serializer.load(Person, {"age": -1, "bio": "foo"})

now = datetime.now()


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    ([Card], [card_dict], [card]),
    (datetime, now, now)
])
def test_schematics_integration_load(serializer, typ, inp, out):
    assert serializer.load(typ, inp) == out


def test_schematics_to_json_schema(serializer):
    assert serializer.to_json_schema(Card) == {
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"}
        },
        "title": "Card",
        "type": "object"
    }


@pytest.mark.parametrize("inp, expected", [
    (UUIDType, {"type": "string", "format": "uuid"}),
    (URLType, {"type": "string", "format": "url"}),
    (StringType, {"type": "string"}),
    (BaseType, {"type": "object"}),
    (datetime, {"type": "string", "format": "date-time"}),
    (Serializable(fget=lambda: None, type=StringType()), {"type": "string"}),
])
def test_to_json_schema(serializer, inp, expected):
    assert serializer.to_json_schema(inp) == expected


def test_schematics_to_json_schema_required_value(serializer):

    class CardNameRequired(Model):
        name = StringType(required=True)
        price = IntType()

    assert serializer.to_json_schema(CardNameRequired) == {
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"}
        },
        "title": "CardNameRequired",
        "required": ["name"],
        "type": "object"
    }


def test_type_not_found_defaults_to_object(serializer):

    class MyType(BaseType):
        pass

    assert serializer.to_json_schema(MyType()) == {
        "type": "object"
    }


def test_non_model_or_primitive_raises_exception(serializer):

    class MyType(object):
        pass

    with pytest.raises(SerializationException):
        serializer.to_json_schema(MyType)


def test_to_json_list(serializer):
    assert serializer.to_json_schema([int]) == {
        "type": "array",
        "items": {"type": "number"}
    }


def test_to_json_dict(serializer):
    assert serializer.to_json_schema(DictType(IntType())) == {
        "type": "object",
        "additionalProperties": {"type": "number"}
    }


def test_serialize_type(serializer):
    """ serializer should be able to serialize a raw type. """
    assert serializer.dump(DictType(StringType()), {"key": "foo"}) == {"key": "foo"}


def test_uuid_serializer(serializer):
    i = uuid.uuid4()
    dumped = serializer.dump(UUIDType, i)
    assert dumped == str(i)
    assert serializer.load(UUIDType, dumped) == i


@pytest.mark.parametrize("cls, should_handle", [
    (int, True),
    (float, True),
    (datetime, True),
    (ModelType(Card), True)
])
def test_can_handle(serializer, cls, should_handle):
    assert serializer.can_handle(cls) == should_handle
