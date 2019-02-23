import json
from aiohttp import web

from transmute_core.swagger import (
    generate_swagger_html,
    get_swagger_static_root,
    SwaggerSpec
)

STATIC_ROOT = "/_swagger/static"
APP_KEY = "_aiohttp_transmute_swagger"


def get_swagger_spec(app):
    if APP_KEY not in app:
        app[APP_KEY] = SwaggerSpec()
    return app[APP_KEY]


def add_swagger(app, json_route, html_route):
    """
    a convenience method for both adding a swagger.json route,
    as well as adding a page showing the html documentation
    """
    app.router.add_route('GET', json_route, create_swagger_json_handler(app))
    add_swagger_api_route(app, html_route, json_route)


def add_swagger_api_route(app, target_route, swagger_json_route):
    """
    mount a swagger statics page.

    app: the aiohttp app object
    target_route: the path to mount the statics page.
    swagger_json_route: the path where the swagger json definitions is
                        expected to be.
    """
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger_html(
        STATIC_ROOT, swagger_json_route
    ).encode("utf-8")

    async def swagger_ui(request):
        return web.Response(body=swagger_body, content_type="text/html")

    app.router.add_route("GET", target_route, swagger_ui)
    app.router.add_static(STATIC_ROOT, static_root)


def create_swagger_json_handler(app, **kwargs):
    """
    Create a handler that returns the swagger definition
    for an application.

    This method assumes the application is using the
    TransmuteUrlDispatcher as the router.
    """

    spec = get_swagger_spec(app).swagger_definition(**kwargs)
    encoded_spec = json.dumps(spec).encode("UTF-8")

    async def swagger(request):
        return web.Response(
            # we allow CORS, so this can be requested at swagger.io
            headers={
                "Access-Control-Allow-Origin": "*"
            },
            body=encoded_spec,
            content_type="application/json",
        )

    return swagger
