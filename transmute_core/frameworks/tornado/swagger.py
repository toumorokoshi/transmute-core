from transmute_core.swagger import (
    generate_swagger_html,
    get_swagger_static_root,
    SwaggerSpec,
)
from transmute_core import default_context
import tornado
import tornado.web

USE_ROUTER = tornado.version_info >= (4, 5)
METHODS = ["get", "post", "delete", "put"]
STATIC_ROOT = "/_swagger/static"


def add_swagger(app, json_route, html_route, context=default_context):
    app.add_handlers(
        ".*",
        [
            (json_route, generate_swagger_json_handler(app, context)),
        ]
        + add_swagger_api_route(html_route, json_route),
    )


def generate_swagger_json_handler(app, context, **kwargs):

    swagger_json = _generate_swagger_json(app, context, **kwargs)

    class SwaggerSpecHandler(tornado.web.RequestHandler):
        def get(self):
            self.write(swagger_json)
            self.finish()

    return SwaggerSpecHandler


def _get_handlers(app):
    if USE_ROUTER:
        for rule in app.wildcard_router.rules:
            yield rule.target
    else:
        for domain, specs in app.handlers:
            for s in specs:
                yield s.handler_class


def _generate_swagger_json(app, context, **kwargs):
    spec = SwaggerSpec()
    for handler in _get_handlers(app):
        for m in METHODS:
            method = getattr(handler, m)
            if hasattr(method, "transmute_func"):
                spec.add_func(method.transmute_func, context)
    return spec.swagger_definition(**kwargs)


def add_swagger_api_route(target_route, swagger_json_route):
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger_html(STATIC_ROOT, swagger_json_route)

    class SwaggerBodyHandler(tornado.web.RequestHandler):
        def get(self):
            self.write(swagger_body)
            self.finish()

    return [
        (target_route, SwaggerBodyHandler),
        (STATIC_ROOT + "/(.*)", tornado.web.StaticFileHandler, {"path": static_root}),
    ]
