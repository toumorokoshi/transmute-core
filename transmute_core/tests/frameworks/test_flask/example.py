from transmute_core.frameworks.flask import (
    route,
    annotate,
    Response,
    APIException,
    add_swagger,
)
from schematics.models import Model
from schematics.types import StringType, IntType
from flask import Flask, Blueprint

app = Flask(__name__)


class Person(Model):
    name = StringType()
    number_of_cats = IntType()


CAT_PEOPLE = {"george": Person({"name": "george", "number_of_cats": 2})}


@route(app, paths="/cat_person")
@annotate({"name": str, "return": Person})
def get_cat_person(name):
    """find and return a cat person"""
    if name in CAT_PEOPLE:
        return CAT_PEOPLE[name]
    raise APIException("no cat person found", code=404)


# alternatively
@route(app, paths="/multiply")
@annotate({"left": int, "right": int, "return": int})
def multiply(left, right):
    """multiply two integers"""
    return left * right


# type hint equivalent in Py2
multiply.__annotations__ = {"left": int, "right": int, "return": int}


@route(app, paths="/exception")
def exception():
    raise APIException("api error!")


@route(
    app,
    paths="/complex/{path}",
    methods=["POST"],
    body_parameters=["body"],
    header_parameters=["header"],
)
@annotate({"body": str, "header": str, "path": str, "return": str})
def complex(body, header, path):
    return body + ":" + header + ":" + path


blueprint = Blueprint("blueprint", __name__, url_prefix="/blueprint")


@route(blueprint, paths="/foo")
@annotate({"return": bool})
def foo():
    return True


@route(blueprint, paths="/test/", methods=["post"], body_parameters="body")
@annotate({"return": bool, "body": Person})
def test(body):
    return True


@route(
    app,
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
    return Response("foo", headers={"x-nothing": "value"})


app.register_blueprint(blueprint)

# finally, you can add a swagger json and a documentation page by:
add_swagger(app, "/swagger.json", "/api/")

if __name__ == "__main__":
    app.run(debug=True)
