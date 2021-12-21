import tornado.testing
import tornado.web
from transmute_core.frameworks.tornado import RouteSet
from transmute_core import describe, annotate, add_swagger
import json


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


@describe(paths="/exception", methods="GET")
def exception(self):
    return raise_exception()


def raise_exception():
    raise Exception("OFOOONTHE")


app = route_set = RouteSet()
route_set.add(get)
route_set.add(add)
route_set.add(subtract)
route_set.add(exception)
app = tornado.web.Application(route_set.generate_url_specs())
add_swagger(app, "/swagger.json", "/swagger")

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
