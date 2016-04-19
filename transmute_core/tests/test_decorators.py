import pytest
from transmute_core.decorators import (
    PUT, POST, DELETE, annotate, TRANSMUTE_HTTP_METHOD_ATTRIBUTE
)


@pytest.mark.parametrize("decorator,method", [
    (PUT, "PUT"),
    (POST, "POST"),
    (DELETE, "DELETE")
])
def test_decorator(decorator, method):

    @decorator
    def test():
        pass

    assert getattr(test, TRANSMUTE_HTTP_METHOD_ATTRIBUTE) == set([method])


def test_joined_decorator():
    """ two decorators together should be merged """

    @POST
    @PUT
    def test():
        pass

    assert getattr(test, TRANSMUTE_HTTP_METHOD_ATTRIBUTE) == set(["POST", "PUT"])


def test_annotate():

    annotations = {"return": str, "arg": int}

    @annotate(annotations)
    def delete_test(arg):
        pass

    assert delete_test.__annotations__ == annotations
