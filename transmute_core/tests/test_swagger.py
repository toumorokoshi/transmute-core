from transmute_core.swagger import (
    generate_swagger_html, get_swagger_static_root,
    SwaggerSpec
)
from transmute_core import default_context


def test_generate_swagger():
    swagger_static_root = "/statics/_swagger"
    swagger_json_url = "/swagger.json"
    body = generate_swagger_html(swagger_static_root, swagger_json_url)
    assert swagger_static_root in body
    assert swagger_json_url in body


def test_get_swagger_static_root():
    assert "static" in get_swagger_static_root()


def test_swagger_definition_generation():
    """
    swagger routes should be ablo to generate a proper
    spec.
    """
    routes = SwaggerSpec()
    assert routes.swagger_definition() == {
        "info": {"title": "example", "version": "1.0"},
        "paths": {},
        "swagger": "2.0",
        "basePath": "/"
    }


def test_swagger_transmute_func(transmute_func):
    """
    swagger routes should be ablo to generate a proper
    spec.
    """
    routes = SwaggerSpec()
    routes.add_func(transmute_func, default_context)
    assert routes.swagger_definition() == {
        "info": {"title": "example", "version": "1.0"},
        "paths": {
            "/api/v1/multiply": transmute_func.get_swagger_path(default_context).to_primitive(),
        },
        "swagger": "2.0",
        "basePath": "/"
    }
