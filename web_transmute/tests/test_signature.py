from web_transmute.compat import getfullargspec
from web_transmute import annotate
from web_transmute.signature import get_signature, NoDefault


def test_signature():

    @annotate({"x": int, "y": float, "width": int, "height": float})
    def make_square(x, y, width=None, height=12):
        pass

    argspec = getfullargspec(make_square)
    signature = get_signature(argspec)
    assert len(signature.arguments) == 2
    assert signature.arguments[0].name == "x"
    assert signature.arguments[0].default == NoDefault
    assert signature.arguments[0].type == int
    assert len(signature.keywords) == 2
    assert signature.keywords["width"].name == "width"
    assert signature.keywords["width"].default is None
    assert signature.keywords["width"].type == int
