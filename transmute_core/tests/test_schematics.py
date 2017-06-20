import uuid
import pytest
from schematics.models import Model
from schematics.types import StringType, IntType, BaseType, UUIDType, URLType, Serializable
from schematics.types.compound import DictType
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
def test_schematics_integration_dump(schematics_serializer, typ, inp, out):
    assert schematics_serializer.dump(typ, inp) == out


def test_schematics_validate_is_called(schematics_serializer):
    with pytest.raises(SerializationException):
        schematics_serializer.load(Person, {"age": -1, "bio": "foo"})


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    ([Card], [card_dict], [card])
])
def test_schematics_integration_load(schematics_serializer, typ, inp, out):
    assert schematics_serializer.load(typ, inp) == out


def test_schematics_to_json_schema(schematics_serializer):
    assert schematics_serializer.to_json_schema(Card) == {
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
    (Serializable(fget=lambda: None, type=StringType()), {"type": "string"}),
])
def test_to_json_schema(schematics_serializer, inp, expected):
    assert schematics_serializer.to_json_schema(inp) == expected


def test_schematics_to_json_schema_required_value(schematics_serializer):

    class CardNameRequired(Model):
        name = StringType(required=True)
        price = IntType()

    assert schematics_serializer.to_json_schema(CardNameRequired) == {
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"}
        },
        "title": "CardNameRequired",
        "required": ["name"],
        "type": "object"
    }


def test_type_not_found_defaults_to_object(schematics_serializer):

    class MyType(BaseType):
        pass

    assert schematics_serializer.to_json_schema(MyType()) == {
        "type": "object"
    }


def test_non_model_or_primitive_raises_exception(schematics_serializer):

    class MyType(object):
        pass

    with pytest.raises(SerializationException):
        schematics_serializer.to_json_schema(MyType)


def test_to_json_list(schematics_serializer):
    assert schematics_serializer.to_json_schema([int]) == {
        "type": "array",
        "items": {"type": "number"}
    }


def test_to_json_dict(schematics_serializer):
    assert schematics_serializer.to_json_schema(DictType(IntType())) == {
        "type": "object",
        "additionalProperties": {"type": "number"}
    }


def test_serialize_type(schematics_serializer):
    """ schematics_serializer should be able to serialize a raw type. """
    assert schematics_serializer.dump(DictType(StringType()), {"key": "foo"}) == {"key": "foo"}


def test_uuid_schematics_serializer(schematics_serializer):
    i = uuid.uuid4()
    dumped = schematics_serializer.dump(UUIDType, i)
    assert dumped == str(i)
    assert schematics_serializer.load(UUIDType, dumped) == i
