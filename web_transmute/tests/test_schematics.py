from schematics.models import Model
from schematics.types import StringType, IntType


def test_schematics_integration(serializer):

    class Card(Model):
        name = StringType()
        description = StringType()
        price = IntType()

    c = Card({
        "name": "foo", "description": "test",
        "price": 10}
    )

    assert serializer.dump(Card, c) == {
        "name": "foo",
        "description": "test",
        "price": 10
    }

    assert serializer.load(Card, {
        "name": "foo",
        "description": "test",
        "price": 10
    }) == c
