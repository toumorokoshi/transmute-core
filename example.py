"""
An example integration with flask.
"""
import json
import sys
import transmute_core
import attr
from transmute_core import (
    describe,
    annotate,
    default_context,
    generate_swagger_html,
    get_swagger_static_root,
    ParamExtractor,
    SwaggerSpec,
    TransmuteFunction,
    NoArgument,
)
from flask import Blueprint, Flask, Response, request
from schematics.models import Model
from schematics.types import StringType
from functools import wraps

SWAGGER_ATTR_NAME = "_tranmute_swagger"
STATIC_PATH = "/_swagger/static"


def transmute_route(app, fn, context=default_context):
    """
    this is the main interface to transmute. It will handle
    adding converting the python function into the a flask-compatible route,
    and adding it to the application.
    """
    transmute_func = TransmuteFunction(fn)
    routes, handler = create_routes_and_handler(transmute_func, context)
    for r in routes:
        """
        the route being attached is a great place to start building up a
        swagger spec.  the SwaggerSpec object handles creating the
        swagger spec from transmute routes for you.

        almost all web frameworks provide some app-specific context
        that one can add values to. It's recommended to attach
        and retrieve the swagger spec from there.
        """
        if not hasattr(app, SWAGGER_ATTR_NAME):
            setattr(app, SWAGGER_ATTR_NAME, SwaggerSpec())
        swagger_obj = getattr(app, SWAGGER_ATTR_NAME)
        swagger_obj.add_func(transmute_func, context)
        app.route(r, methods=transmute_func.methods)(handler)


def create_routes_and_handler(transmute_func, context):
    """
    return back a handler that is the api generated
    from the transmute_func, and a list of routes
    it should be mounted to.
    """

    @wraps(transmute_func.raw_func)
    def handler():
        exc, result = None, None
        try:
            args, kwargs = ParamExtractorFlask().extract_params(
                context, transmute_func, request.content_type
            )
            result = transmute_func(*args, **kwargs)
        except Exception as e:
            exc = e
            """
            attaching the traceack is done for you in Python 3, but
            in Python 2 the __traceback__ must be
            attached to the object manually.
            """
            exc.__traceback__ = sys.exc_info()[2]
        """
        transmute_func.process_result handles converting
        the response from the function into the response body,
        the status code that should be returned, and the
        response content-type.
        """
        response = transmute_func.process_result(
            context, result, exc, request.content_type
        )
        return Response(
            response["body"],
            status=response["code"],
            mimetype=response["content-type"],
            headers=response["headers"],
        )

    return (_convert_paths_to_flask(transmute_func.paths), handler)


def _convert_paths_to_flask(transmute_paths):
    """
    convert transmute-core's path syntax (which uses {var} as the
    variable wildcard) into flask's <var>.
    """
    paths = []
    for p in transmute_paths:
        paths.append(p.replace("{", "<").replace("}", ">"))
    return paths


class ParamExtractorFlask(ParamExtractor):
    """
    The code that converts http parameters into function signature
    arguments is complex, so the abstract class ParamExtractor is
    provided as a convenience.

    override the methods to complete the class.
    """

    def __init__(self, *args, **kwargs):
        """
        in the case of flask, this is blank. But it's common
        to pass request-specific variables in the ParamExtractor,
        to be used in the methods.
        """
        super(ParamExtractorFlask, self).__init__(*args, **kwargs)

    def _get_framework_args(self):
        """
        this method should return back a dictionary of the values that
        are normally passed into the handler (e.g. the "request" object
        in aiohttp).

        in the case of flask, this is blank.
        """
        return {}

    @property
    def body(self):
        return request.get_data()

    @staticmethod
    def _query_argument(key, is_list):
        if key not in request.args:
            return NoArgument
        if is_list:
            return request.args.getlist(key)
        else:
            return request.args[key]

    @staticmethod
    def _header_argument(key):
        return request.headers.get(key, NoArgument)

    @staticmethod
    def _path_argument(key):
        return request.match_info.get(key, NoArgument)


def add_swagger(app, json_route, html_route, **kwargs):
    """
    add a swagger html page, and a swagger.json generated
    from the routes added to the app.
    """
    spec = getattr(app, SWAGGER_ATTR_NAME)
    if spec:
        spec = spec.swagger_definition(**kwargs)
    else:
        spec = {}
    encoded_spec = json.dumps(spec).encode("UTF-8")

    @app.route(json_route)
    def swagger():
        return Response(
            encoded_spec,
            # we allow CORS, so this can be requested at swagger.io
            headers={"Access-Control-Allow-Origin": "*"},
            content_type="application/json",
        )

    # add the statics
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger_html(STATIC_PATH, json_route).encode("utf-8")

    @app.route(html_route)
    def swagger_ui():
        return Response(swagger_body, content_type="text/html")

    # the blueprint work is the easiest way to integrate a static
    # directory into flask.
    blueprint = Blueprint(
        "swagger", __name__, static_url_path=STATIC_PATH, static_folder=static_root
    )
    app.register_blueprint(blueprint)


# example usage.


@describe(
    paths="/api/v1/multiply/{document_id}",
    header_parameters=["header"],
    body_parameters="foo",
)
@annotate(
    {
        "left": int,
        "right": int,
        "header": int,
        "foo": str,
        "return": int,
        "document_id": str,
    }
)
def multiply(left, right, foo, document_id, header=0):
    return left * right


@describe(paths="/api/v1/multiply_body", body_parameters="body")
@annotate({"body": int})
def multiply_body(body):
    return left * right


@describe(paths="/api/v1/test")
@annotate({"vals": [int], "return": [int]})
def foo(vals):
    return vals


class SchematicsBody(Model):
    name = StringType(max_length=5)


@describe(
    paths="/api/v1/schematics", methods=["POST"], tags=["foo"], body_parameters="body"
)
@annotate({"body": SchematicsBody})
def schematics_example(body):
    return None


@describe(
    paths="/api/v1/header",
    response_types={
        200: {
            "type": str,
            "description": "success",
            "headers": {
                "location": {"description": "url to the location", "type": str}
            },
        },
    },
)
def header():
    return transmute_core.Response("foo", headers={"x-nothing": "value"})


@attr.s
class AttrsExample(object):
    foo = attr.ib(type=str)


@describe(paths="/api/v1/attrs")
@annotate({"return": AttrsExample})
def attrs():
    return AttrsExample(foo="bar")


app = Flask(__name__)
app = Flask(__name__)
transmute_route(app, attrs)
transmute_route(app, multiply)
transmute_route(app, multiply_body)
transmute_route(app, schematics_example)
transmute_route(app, foo)
transmute_route(app, header)
add_swagger(app, "/api/swagger.json", "/api/")

if __name__ == "__main__":
    app.run(debug=True)
