import pytest
from schematics.models import Model
from schematics.types import StringType, IntType, BaseType
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
def test_schematics_integration_dump(serializer, typ, inp, out):
    assert serializer.dump(typ, inp) == out


def test_schematics_validate_is_called(serializer):
    with pytest.raises(SerializationException):
        serializer.load(Person, {"age": -1, "bio": "foo"})


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    ([Card], [card_dict], [card])
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


def test_type_not_found_defaults_to_string(serializer):

    class MyType(BaseType):
        pass

    assert serializer.to_json_schema(MyType()) == {
        "type": "string"
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
