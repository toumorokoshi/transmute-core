from transmute_core import describe, default_context, TransmuteFunction
from transmute_core.swagger import SwaggerSpec
from .handler import create_routes_and_handler
from .swagger import SWAGGER_ATTR_NAME


def route(app_or_blueprint, context=default_context, **kwargs):
    """attach a transmute route."""

    def decorator(fn):
        fn = describe(**kwargs)(fn)
        transmute_func = TransmuteFunction(fn)
        routes, handler = create_routes_and_handler(transmute_func, context)
        for r in routes:
            # push swagger info.
            if not hasattr(app_or_blueprint, SWAGGER_ATTR_NAME):
                setattr(app_or_blueprint, SWAGGER_ATTR_NAME, SwaggerSpec())
            swagger_obj = getattr(app_or_blueprint, SWAGGER_ATTR_NAME)
            swagger_obj.add_func(transmute_func, context)
            app_or_blueprint.route(r, methods=transmute_func.methods)(handler)
        return handler

    return decorator
