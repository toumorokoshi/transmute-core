import pytest
from transmute_core import annotate, describe
from transmute_core.compat import getfullargspec
from transmute_core.function.signature import FunctionSignature
from transmute_core.function.parameters import (
    get_parameters,
    _extract_path_parameters_from_paths,
)
from transmute_core.attributes import TransmuteAttributes
from transmute_core.exceptions import InvalidTransmuteDefinition


def test_get_argument_set():
    @describe(paths="/{x}", body_parameters=["y"])
    @annotate({"x": int, "y": float, "z": int, "width": int, "height": float})
    def make_square(x, y, z, width=None, height=12):
        pass

    argspec = getfullargspec(make_square)
    signature = FunctionSignature.from_argspec(argspec)
    argument_sets = get_parameters(signature, make_square.transmute)
    assert ["y"] == list(argument_sets.body.keys())
    assert set(["x"]) == set(argument_sets.path.keys())
    assert set(["z", "width", "height"]) == set(argument_sets.query.keys())


def test_ignore_request_parameter():
    @annotate({"x": int, "y": int})
    def handle_request(request, x, y):
        pass

    argspec = getfullargspec(handle_request)
    signature = FunctionSignature.from_argspec(argspec)
    params = get_parameters(
        signature, TransmuteAttributes(), arguments_to_ignore=["request"]
    )
    for typ in ["query", "body", "header", "path"]:
        assert "request" not in getattr(params, typ)


@pytest.mark.parametrize(
    "invalid_paths, expected",
    [
        (["/foo/{bar}/baz", "/foo/{baz}/bar"], {"bar", "baz"}),
        (["/foo/{bar}/baz", "/foo/{bar}/bar/{extra}"], {"bar", "extra"}),
    ],
)
def test_non_matching_path_parameters(invalid_paths, expected):
    """with non matching paths, the whole set of values should be used."""
    assert _extract_path_parameters_from_paths(invalid_paths) == expected


@pytest.mark.parametrize("paths, params", [([], [])])
def test_param_list(paths, params):
    assert _extract_path_parameters_from_paths(paths) == set(params)
