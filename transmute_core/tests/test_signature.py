from transmute_core.compat import getfullargspec
from transmute_core import annotate
from transmute_core.function.signature import (
    FunctionSignature,
    NoDefault
)


def test_signature():

    @annotate({"x": int, "y": float, "width": int, "height": float})
    def make_square(x, y, width=None, height=12):
        pass

    argspec = getfullargspec(make_square)
    signature = FunctionSignature.from_argspec(argspec)
    assert len(signature.args) == 2
    assert signature.args[0].name == "x"
    assert signature.args[0].default == NoDefault
    assert signature.args[0].type == int
    assert len(signature.kwargs) == 2
    assert signature.kwargs["width"].name == "width"
    assert signature.kwargs["width"].default is None
    assert signature.kwargs["width"].type == int


def test_signature_no_kwargs():

    @annotate({"x": int, "y": int, "return": int})
    def make_square(x, y):
        return x * y

    argspec = getfullargspec(make_square)
    signature = FunctionSignature.from_argspec(argspec)
    assert len(signature.args) == 2
    assert signature.args[0].name == "x"
    assert signature.args[0].default == NoDefault
    assert signature.args[0].type == int
    assert signature.args[1].name == "y"
    assert signature.args[1].default == NoDefault
    assert signature.args[1].type == int
    assert len(signature.kwargs) == 0


def test_self_signature():

    def square(self, resource, multiplier=None):
        pass

    argspec = getfullargspec(square)
    signature = FunctionSignature.from_argspec(argspec)

    assert len(signature.args) == 1
    assert len(signature.kwargs) == 1
    assert signature.kwargs["multiplier"].name == "multiplier"


def test_get_signature():

    def square(self, resource, multiplier=None):
        pass

    argspec = getfullargspec(square)
    signature = FunctionSignature.from_argspec(argspec)

    arg = signature.get_argument("resource")
    assert arg.name == "resource"

    kwarg = signature.get_argument("multiplier")
    assert kwarg.name == "multiplier"
