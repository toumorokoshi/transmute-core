import warnings
from aiohttp.web import UrlDispatcher
from collections import OrderedDict
from transmute_core import default_context, describe
from transmute_core.function import TransmuteFunction
from transmute_core.swagger import SwaggerSpec
from .route import add_route


class TransmuteUrlDispatcher(UrlDispatcher):
    """
    .. warning:: The TransmuteUrlDispatcher is deprecated.
                 please use aiohttp_transmute.add_route instead.

    A UrlDispatcher which instruments the add_route function to
    collect swagger spec data from transmuted functions.
    """

    def __init__(self, *args, context=default_context, **kwargs):
        warnings.warn(
            (
                "TransmuteUrlDispatch has been deprecated. "
                " And will be removed in a future version. "
                " Please use aiohttp_transmute.add_route instead. "
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()
        self._transmute_context = context

    def post_init(self, app):
        """
        this must be called after dispatcher creation, to ensure proper operability.
        """
        self._app = app

    def add_transmute_route(self, *args):
        """
        two formats are accepted, for transmute routes. One allows
        for a more traditional aiohttp syntax, while the other
        allows for a flask-like variant.

        .. code-block:: python

            # if the path and method are not added in describe.
            add_transmute_route("GET", "/route", fn)

            # if the path and method are already added in describe
            add_transmute_route(fn)
        """
        if len(args) == 1:
            fn = args[0]
        elif len(args) == 3:
            methods, paths, fn = args
            fn = describe(methods=methods, paths=paths)(fn)
        else:
            raise ValueError("expected one or three arguments for add_transmute_route!")

        add_route(self._app, fn, context=self._transmute_context)
