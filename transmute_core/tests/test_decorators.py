import pytest

from transmute_core.decorators import (
    describe, annotate
)


@pytest.mark.parametrize("method", [
    "PUT", "POST", "DELETE"
])
def test_describe(method):

    @describe(methods=method)
    def test():
        pass

    assert test.transmute.methods == set([method])


def test_describe_join():
    """ two describe annotations should merge the descriptions """
    @describe(methods=["GET"])
    @describe(methods=["PUT"])
    def test():
        pass

    assert test.transmute.methods == set(["GET", "PUT"])


def test_annotate():

    annotations = {"return": str, "arg": int}

    @annotate(annotations)
    def delete_test(arg):
        pass

    assert delete_test.__annotations__ == annotations
