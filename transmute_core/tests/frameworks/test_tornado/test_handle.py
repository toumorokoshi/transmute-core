import tornado.testing
import tornado.web
from transmute_core import describe, annotate
from transmute_core.frameworks.tornado import RouteSet, add_swagger
import json

# frameworks.tornado also provides a RouteSet, which can output tornado-compatible url objects.
# this provides a more flask-like approach, and handles combining routes which have the same path


@describe(paths="/foo/{multiplier}")
@annotate({"multiplier": int, "return": int})
def get(self, multiplier):
    return 2 * multiplier


@describe(paths="/add")
@annotate({"left": int, "right": int, "return": int})
def add(self, left, right):
    return left + right


@describe(paths="/add", methods="POST")
@annotate({"left": int, "right": int, "return": int})
def subtract(self, left, right):
    return left - right


class TestApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        route_set = RouteSet()
        route_set.add(get)
        route_set.add(add)
        route_set.add(subtract)
        app = tornado.web.Application(route_set.generate_url_specs())
        add_swagger(app, "/swagger.json", "/swagger")
        return app

    def test_foo(self):
        resp = self.fetch("/foo/1")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json == 2

    def test_queryparam(self):
        resp = self.fetch("/add?left=1&right=10")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json == 11

    def test_missing_arg(self):
        resp = self.fetch("/add?left=1")
        assert resp.code == 400

    def test_body(self):
        resp = self.fetch(
            "/add",
            method="POST",
            body=json.dumps({"left": 10, "right": 2}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json == 8

    def test_swagger_json(self):
        resp = self.fetch("/swagger.json")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert "get" in resp_json["paths"]["/foo/{multiplier}"]
        assert resp_json["swagger"] == "2.0"
        assert resp_json["info"] == {"title": "example", "version": "1.0"}

    def test_swagger_body(self):
        resp = self.fetch("/swagger")
        assert resp.code == 200
        body = resp.body.decode("UTF-8")
        assert "End Swagger" in body
