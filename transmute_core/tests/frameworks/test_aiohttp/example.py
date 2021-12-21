from aiohttp import web
from transmute_core.frameworks.aiohttp import (
    describe,
    add_swagger,
    add_route,
    route,
    APIException,
    Response,
)
from aiohttp.web import HTTPForbidden
from .utils import User


async def handle(request):
    text = "Hello, can you hear me?"
    return web.Response(body=text.encode("utf-8"))


@describe(paths="/multiply")
async def multiply(request, left: int, right: int) -> int:
    return left * right


@describe(paths="/id/{my_id}")
async def get_id(request, my_id: str) -> str:
    return "your id is: " + my_id


@describe(paths="/optional")
async def get_optional(request, include_foo: bool = False) -> bool:
    return include_foo


@describe(
    paths="/headers/",
    response_types={
        200: {
            "type": str,
            "description": "success",
            "headers": {
                "location": {"description": "url to the location", "type": str}
            },
        }
    },
)
async def header_response(request):
    return Response("foo", headers={"location": "boo"})


@describe(paths="/aiohttp_error")
async def error(request):
    raise HTTPForbidden(reason="unauthorized")


@describe(paths="/api_exception")
async def api_exception(request) -> User:
    raise APIException("nope")


@describe(
    paths="/body_and_header",
    methods="POST",
    body_parameters=["body"],
    header_parameters=["header"],
)
async def body_and_header(request, body: str, header: str) -> bool:
    return body == header


@describe(paths="/config")
async def config(request):
    return request.app["config"]


@describe(paths="/multiple_query_params")
async def multiple_query_params(tag: [str]) -> str:
    return ",".join(tag)


def create_app():
    app = web.Application()
    app["config"] = {"test": "foo"}
    app.router.add_route("GET", "/", handle)
    add_route(app, multiple_query_params)
    add_route(app, multiply)
    add_route(app, get_id)
    add_route(app, header_response)
    route(app, config)
    route(app, get_optional)
    route(app, body_and_header)
    route(app, error)
    route(app, api_exception)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    add_swagger(app, "/swagger.json", "/swagger")
    return app
