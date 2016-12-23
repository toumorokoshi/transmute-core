import os
import jinja2
from swagger_schema import Swagger, Info

CURDIR = os.path.dirname(__file__)


def generate_swagger(swagger_static_root, swagger_json_url):
    """
    given a root directory for the swagger statics, and
    a swagger json path, return back a swagger html designed
    to use those values.
    """
    tmpl = get_template("swagger.html")
    return tmpl.render(
        swagger_root=swagger_static_root,
        swagger_json_url=swagger_json_url
    )


def get_swagger_static_root():
    return os.path.join(CURDIR, "static")

_template_cache = {}


def get_template(template_name):
    if template_name not in _template_cache:
        template_path = os.path.join(CURDIR, template_name)
        with open(template_path) as fh:
            _template_cache[template_name] = jinja2.Template(fh.read())
    return _template_cache[template_name]


class SwaggerSpec(object):
    """
    a class for aggregating and outputting swagger definitions, from
    transmute primitives
    """

    def __init__(self):
        self._swagger = {}

    def add_func(self, transmute_func, transmute_context):
        """ add a transmute function's swagger definition to the spec """
        swagger_path = transmute_func.get_swagger_path(transmute_context)
        for p in transmute_func.paths:
            if p not in self._swagger:
                self._swagger[p] = swagger_path
            else:
                for method, definition in swagger_path.items():
                    setattr(self._swagger[p], method, definition)

    @property
    def paths(self):
        """
        return the path section of the final swagger spec,
        aggregated from the paths added.
        """
        return self._swagger

    def swagger_definition(self, title="example", version="1.0"):
        """ return a valid swagger definition """
        return Swagger({
            "info": Info({"title": title, "version": version}),
            "paths": self.paths,
            "swagger": "2.0",
            "basePath": "/",
        }).to_primitive()
