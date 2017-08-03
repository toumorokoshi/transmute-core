import pytest
import attr
import cattr
from transmute_core.exceptions import SerializationException
from cattr.vendor.typing import List


class Player(object):
    
    def __init__(self, name, score):
        self.name = name
        self.score = score


@attr.s
class Card(object):
    name = attr.ib(default="")
    price = attr.ib(default=1.0)


@attr.s
class Person(object):
    age = attr.ib()
    bio = attr.ib(default="")

    @age.validator
    def greater_than_zero(self, attribute, value):
        if value < 0:
            raise ValueError("must be greater than zero")
        return value


card_dict = {"name": "foo", "price": 10}
card = Card(**card_dict)
player = Player("kobe", 81)


@pytest.mark.parametrize("inp,out", [
    (card, card_dict),
    ([card], [card_dict]),
    (player, player)
])
def test_attrs_integration_dump(attrs_serializer, inp, out):
    assert attrs_serializer.dump(inp) == out


def test_attrs_integration_dump_exception(monkeypatch, attrs_serializer):
    def mock_return(inp):
        raise ValueError("Random_Exception")
    monkeypatch.setattr(cattr, "unstructure", mock_return)
    with pytest.raises(SerializationException):
        assert attrs_serializer.dump("random_str")


@pytest.mark.parametrize("typ,inp", [
    ([Card], [card_dict])
])
def test_attrs_integration_load_exception(attrs_serializer, typ, inp):
    with pytest.raises(SerializationException):
        attrs_serializer.load(typ, inp)


def test_attrs_validate_is_called(attrs_serializer):
    with pytest.raises(SerializationException):
        attrs_serializer.load(Person, {"age": -1, "bio": "foo"})


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    (List[Card], [card_dict], [card]),
])
def test_attrs_integration_load(attrs_serializer, typ, inp, out):
    assert attrs_serializer.load(typ, inp) == out
