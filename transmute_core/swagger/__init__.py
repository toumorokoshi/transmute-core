import os

from swagger_schema import Swagger, Info
from .template import Template


CURDIR = os.path.dirname(__file__)


def generate_swagger_html(swagger_static_root, swagger_json_url):
    """
    given a root directory for the swagger statics, and
    a swagger json path, return back a swagger html designed
    to use those values.
    """
    tmpl = _get_template("swagger.html")
    return tmpl.render(
        swagger_root=swagger_static_root, swagger_json_url=swagger_json_url
    )


def get_swagger_static_root():
    """
    transmute-core includes the statics to render
    a swagger page. Use this function to
    return the directory containing said statics.
    """
    return os.path.join(CURDIR, "static")


_template_cache = {}


def _get_template(template_name):
    if template_name not in _template_cache:
        template_path = os.path.join(CURDIR, template_name)
        with open(template_path) as fh:
            _template_cache[template_name] = Template(fh.read())
    return _template_cache[template_name]


class SwaggerSpec(object):
    """
    a class for aggregating and outputting swagger definitions, from
    transmute primitives
    """

    DEFAULT_INFO = {"title": "example", "version": "1.0"}

    def __init__(self):
        self._swagger = {}

    def add_func(self, transmute_func, transmute_context):
        """add a transmute function's swagger definition to the spec"""
        swagger_path = transmute_func.get_swagger_path(transmute_context)
        for p in transmute_func.paths:
            self.add_path(p, swagger_path)

    def add_path(self, path, path_item):
        """for a given path, add the path items."""
        if path not in self._swagger:
            self._swagger[path] = path_item
        else:
            for method, definition in path_item.items():
                if definition is not None:
                    setattr(self._swagger[path], method, definition)

    @property
    def paths(self):
        """
        return the path section of the final swagger spec,
        aggregated from the paths added.
        """
        return self._swagger

    def swagger_definition(self, base_path=None, **kwargs):
        """
        return a valid swagger spec, with the values passed.
        """
        return Swagger(
            {
                "info": Info(
                    {
                        key: kwargs.get(key, self.DEFAULT_INFO.get(key))
                        for key in Info.fields.keys()
                        if key in kwargs or key in self.DEFAULT_INFO
                    }
                ),
                "paths": self.paths,
                "swagger": "2.0",
                "basePath": base_path,
            }
        ).to_primitive()
