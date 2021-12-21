from .handler import convert_to_handler
from .url import url_spec
from transmute_core import default_context
import tornado.web


class RouteSet(object):
    def __init__(self, context=default_context):
        self._handler_by_path = {}
        self._context = context

    def add(self, func):
        handler = convert_to_handler(self._context)(func)
        transmute_func = handler.transmute_func
        for p in transmute_func.paths:
            if p not in self._handler_by_path:

                class TransmuteRequestHandler(tornado.web.RequestHandler):
                    pass

                self._handler_by_path[p] = TransmuteRequestHandler
            request_class = self._handler_by_path[p]
            for method in transmute_func.methods:
                setattr(request_class, method.lower(), handler)

    def generate_url_specs(self):
        routes = []
        for path, handler in self._handler_by_path.items():
            routes.append(url_spec(path, handler))
        return routes
