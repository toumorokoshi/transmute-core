import json
from flask import Flask, Blueprint
from transmute_core.frameworks.flask.swagger import SWAGGER_ATTR_NAME
from transmute_core.frameworks.flask import route, add_swagger


def test_blueprint_only_app():
    """
    A flask app that only has transmute routes
    in blueprints should be valide.
    """
    app = Flask(__name__)
    blueprint = Blueprint("foo", __name__)

    # this also unit tests empty url prefix blueprints.
    @route(blueprint, paths=["/foo"])
    def foo():
        return None

    app.register_blueprint(blueprint)
    add_swagger(app, "/swagger.json", "/swagger")

    test_client = app.test_client()
    body = json.loads(test_client.get("/swagger.json").data.decode())
    assert "/foo" in body["paths"]
