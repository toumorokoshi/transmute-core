"""
tests for legacy url dispatcher.
"""
import pytest
from transmute_core.frameworks.aiohttp.url_dispatcher import TransmuteUrlDispatcher
from transmute_core.frameworks.aiohttp.swagger import get_swagger_spec
from transmute_core import describe
from unittest.mock import patch


async def describe_later() -> str:
    return "foo"


@describe(paths="/describe_now")
async def describe_now() -> str:
    return "foo"


@pytest.fixture
def url_dispatcher(app):
    dispatcher = TransmuteUrlDispatcher()
    dispatcher.post_init(app)
    return dispatcher


def test_urldispatcher_exception_invalid_argcount(url_dispatcher):
    with pytest.raises(ValueError):
        url_dispatcher.add_transmute_route(1, 2, 3, 4)


def test_urldispatcher_adds_route(app, url_dispatcher):
    with patch(
        "transmute_core.frameworks.aiohttp.url_dispatcher.add_route"
    ) as add_route:
        url_dispatcher.add_transmute_route("GET", "/describe_later", describe_later)
        assert "GET" in describe_later.transmute.methods
        assert "/describe_later" in describe_later.transmute.paths
        add_route.assert_called_with(
            app, describe_later, context=url_dispatcher._transmute_context
        )


def test_urldispatcher_adds_route_one_arg(app, url_dispatcher):
    with patch(
        "transmute_core.frameworks.aiohttp.url_dispatcher.add_route"
    ) as add_route:
        url_dispatcher.add_transmute_route(describe_now)
        add_route.assert_called_with(
            app, describe_now, context=url_dispatcher._transmute_context
        )
