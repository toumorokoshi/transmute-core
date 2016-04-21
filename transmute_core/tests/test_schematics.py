import pytest
from schematics.models import Model
from schematics.types import StringType, IntType


class Card(Model):
    name = StringType()
    price = IntType()

card_dict = {"name": "foo", "price": 10}
card = Card(card_dict)


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card, card_dict),
    ([Card], [card], [card_dict])
])
def test_schematics_integration_dump(serializer, typ, inp, out):
    assert serializer.dump(typ, inp) == out


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    ([Card], [card_dict], [card])
])
def test_schematics_integration_load(serializer, typ, inp, out):
    assert serializer.load(typ, inp) == out
