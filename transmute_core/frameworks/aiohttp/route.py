from transmute_core import TransmuteFunction, default_context
from .handler import create_handler
from .swagger import get_swagger_spec


def add_route(app, fn, context=default_context):
    """
    a decorator that adds a transmute route to the application.
    """
    transmute_func = TransmuteFunction(
        fn,
        args_not_from_request=["request"]
    )
    handler = create_handler(transmute_func, context=context)
    get_swagger_spec(app).add_func(transmute_func, context)

    for p in transmute_func.paths:
        aiohttp_path = _convert_to_aiohttp_path(p)
        resource = app.router.add_resource(aiohttp_path)
        for method in transmute_func.methods:
            resource.add_route(method, handler)


def _convert_to_aiohttp_path(path):
    """ convert a transmute path to one supported by aiohttp. """
    return path
