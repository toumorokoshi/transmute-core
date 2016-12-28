import re
from ..exceptions import InvalidTransmuteDefinition


class Parameters(object):
    def __init__(self, query=None, body=None, header=None, path=None):
        self.query = query or {}
        self.body = body or {}
        self.header = header or {}
        self.path = path or {}


def get_parameters(signature, transmute_attrs, arguments_to_ignore=None):
    """given a function, categorize which arguments should be passed by
    what types of parameters. The choices are:

    * query parameters: passed in as query parameters in the url
    * body parameters: retrieved from the request body (includes forms)
    * header parameters: retrieved from the request header
    * path parameters: retrieved from the uri path

    The categorization is performed for an argument "arg" by:

    1. examining the transmute parameters attached to the function (e.g.
    func.transmute_query_parameters), and checking if "arg" is mentioned. If so,
    it is added to the category.

    2. If the argument is available in the path, it will be added
    as a path parameter.

    3. If the method of the function is GET and only GET, then "arg" will be
    be added to the expected query parameters. Otherwise, "arg" will be added as
    a body parameter.
    """
    arguments_to_ignore = arguments_to_ignore or []
    params = Parameters()
    used_keys = set()
    # examine what variables are categorized first.
    for key in ["query", "body", "header", "path"]:
        explicit_parameters = getattr(transmute_attrs, key + "_parameters")
        for name in explicit_parameters:
            getattr(params, key)[name] = signature.get_argument(name)
            used_keys.add(name)

    # extract the parameters from the paths
    for name in _extract_path_parameters_from_paths(transmute_attrs.paths):
        params.path[name] = signature.get_argument(name)
        used_keys.add(name)

    # check the method type, and decide if the parameters should be extracted
    # from query parameters or the body
    default_param_key = (
        "query" if transmute_attrs.methods == set(["GET"]) else "body"
    )
    default_params = getattr(params, default_param_key)

    # parse all positional params
    for arg in signature.args:
        if arg.name in arguments_to_ignore:
            continue
        if arg.name in used_keys:
            continue
        used_keys.add(arg.name)
        default_params[arg.name] = arg

    for name, arg in signature.kwargs.items():
        if name in arguments_to_ignore:
            continue
        if name in used_keys:
            continue
        used_keys.add(name)
        default_params[name] = arg

    return params

PART_REGEX = re.compile(r'(\{[_a-zA-Z][^{}]*(?:\{[^{}]*\}[^{}]*)*\})')
PARAM_REGEX = re.compile(r'^\{(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\}$')


def _extract_path_parameters_from_paths(paths):
    """
    from a list of paths, return back a list of the
    arguments present in those paths.

    the arguments available in all of the paths must match: if not,
    an exception will be raised.
    """
    params = None
    for path in paths:
        current_params = set()
        parts = PART_REGEX.split(path)
        for p in parts:
            match = PARAM_REGEX.match(p)
            if match:
                current_params.add(match.group("name"))
        if params is None:
            params = current_params
        elif params != current_params:
            raise InvalidTransmuteDefinition(
                "paths {0} do not match in the parameters they can support.".format(paths)
            )
    return params or set()
