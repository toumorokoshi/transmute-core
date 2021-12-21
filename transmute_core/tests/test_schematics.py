import uuid
import pytest
from datetime import datetime
from schematics.models import Model
from schematics.types import (
    StringType,
    IntType,
    BaseType,
    UUIDType,
    URLType,
    Serializable,
    UTCDateTimeType,
)
from schematics.types.compound import DictType, ModelType
from schematics.exceptions import ValidationError
from transmute_core.exceptions import SerializationException, NoSerializerFound
from transmute_core.object_serializers.schematics_serializer import SchematicsSerializer


class Card(Model):
    name = StringType()
    price = IntType()


def greater_than_zero(value):
    if value < 0:
        raise ValidationError("must be greater than zero")
    return value


class Person(Model):
    age = IntType(required=True, validators=[greater_than_zero])
    bio = StringType(max_length=5)


card_dict = {"name": "foo", "price": 10}
card = Card(card_dict)


@pytest.mark.parametrize(
    "typ,inp,out", [(Card, card, card_dict), ([Card], [card], [card_dict])]
)
def test_schematics_integration_dump(object_serializer_set, typ, inp, out):
    assert object_serializer_set.dump(typ, inp) == out


@pytest.mark.parametrize(
    "typ, bad_data",
    [
        (Person, {"age": -1, "bio": "foo"}),
        (Person, {"age": 20, "bio": "fooooooooo"}),
        (StringType(max_length=4), "foooooo"),
    ],
)
def test_schematics_validate_is_called(object_serializer_set, typ, bad_data):
    with pytest.raises(SerializationException):
        object_serializer_set.load(typ, bad_data)


now = datetime.now()


@pytest.mark.parametrize(
    "typ,inp,out",
    [(Card, card_dict, card), ([Card], [card_dict], [card]), (datetime, now, now)],
)
def test_schematics_integration_load(object_serializer_set, typ, inp, out):
    assert object_serializer_set.load(typ, inp) == out


def test_schematics_to_json_schema(object_serializer_set):
    assert object_serializer_set.to_json_schema(Card) == {
        "properties": {"name": {"type": "string"}, "price": {"type": "integer"}},
        "title": "Card",
        "type": "object",
    }


@pytest.mark.parametrize(
    "inp, expected",
    [
        (UUIDType, {"type": "string", "format": "uuid"}),
        (URLType, {"type": "string", "format": "url"}),
        (StringType, {"type": "string"}),
        (BaseType, {"type": "object"}),
        (IntType, {"type": "integer"}),
        (datetime, {"type": "string", "format": "date-time"}),
        (UTCDateTimeType, {"type": "string", "format": "date-time"}),
        (Serializable(fget=lambda: None, type=StringType()), {"type": "string"}),
    ],
)
def test_to_json_schema(object_serializer_set, inp, expected):
    assert object_serializer_set.to_json_schema(inp) == expected


def test_schematics_to_json_schema_required_value(object_serializer_set):
    class CardNameRequired(Model):
        name = StringType(required=True)
        price = IntType()

    assert object_serializer_set.to_json_schema(CardNameRequired) == {
        "properties": {"name": {"type": "string"}, "price": {"type": "integer"}},
        "title": "CardNameRequired",
        "required": ["name"],
        "type": "object",
    }


def test_type_not_found_defaults_to_object(object_serializer_set):
    class MyType(BaseType):
        pass

    assert object_serializer_set.to_json_schema(MyType()) == {"type": "object"}


def test_non_model_or_primitive_raises_exception(object_serializer_set):
    class MyType(object):
        pass

    with pytest.raises(NoSerializerFound):
        object_serializer_set.to_json_schema(MyType)


def test_to_json_list(object_serializer_set):
    assert object_serializer_set.to_json_schema([int]) == {
        "type": "array",
        "items": {"type": "integer"},
    }


def test_to_json_dict(object_serializer_set):
    assert object_serializer_set.to_json_schema(DictType(IntType())) == {
        "type": "object",
        "additionalProperties": {"type": "integer"},
    }


def test_serialize_type(object_serializer_set):
    """object_serializer_set should be able to serialize a raw type."""
    assert object_serializer_set.dump(DictType(StringType()), {"key": "foo"}) == {
        "key": "foo"
    }


def test_dict_type_object_serializer_set(object_serializer_set):
    """serializer should be able to serialize a raw type."""
    assert object_serializer_set.dump(DictType(StringType()), {"key": "foo"}) == {
        "key": "foo"
    }


def test_uuid_serializer(object_serializer_set):
    i = uuid.uuid4()
    dumped = object_serializer_set.dump(UUIDType, i)
    assert dumped == str(i)
    assert object_serializer_set.load(UUIDType, dumped) == i


@pytest.mark.parametrize(
    "cls, should_handle",
    [(int, True), (float, True), (datetime, True), (ModelType(Card), True)],
)
def test_can_handle(object_serializer_set, cls, should_handle):
    """
    the object serializer set should not raise an exception if it can handle these types.
    """
    object_serializer_set[cls]


def test_schematics_uses_cached_entries():
    """
    Regression test. Validating that SchematicsSerializer uses the
    same json schema it used previously, as before erroneous
    use of the instantiated model as a key was causing memory leaks.
    """
    serializer = SchematicsSerializer()
    # A nested schema type is required as primitives have
    # hard-coded dictionaries representing the json.
    class SchematicsBody(Model):
        name = StringType(max_length=5)

    # ensure that instances have the same key as well.
    instance = ModelType(SchematicsBody)
    original_payload = serializer.to_json_schema(instance)
    second_payload = serializer.to_json_schema(instance)
    assert original_payload is second_payload

    # classes are also valid output to recieve that the json schema
    original_payload = serializer.to_json_schema(SchematicsBody)
    second_payload = serializer.to_json_schema(SchematicsBody)
    assert original_payload is second_payload
