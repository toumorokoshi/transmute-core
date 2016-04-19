import os
import jinja2

CURDIR = os.path.dirname(__file__)


def generate_swagger(swagger_static_root, swagger_json_url):
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
