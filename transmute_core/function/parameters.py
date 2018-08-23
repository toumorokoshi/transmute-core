import re
from ..http_parameters import Parameters, ParamSet, Param
from ..exceptions import InvalidTransmuteDefinition


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
    params = Parameters()
    used_keys = set(arguments_to_ignore or [])
    # examine what variables are categorized first.
    for key in ["query", "header", "path"]:
        param_set = getattr(params, key)
        explicit_parameters = getattr(transmute_attrs, key + "_parameters")
        used_keys |= load_parameters(
            param_set, explicit_parameters, signature, transmute_attrs
        )

    body_parameters = transmute_attrs.body_parameters
    if isinstance(body_parameters, str):
        name = body_parameters
        params.body = Param(
            argument_name=name,
            description=transmute_attrs.parameter_descriptions.get(name),
            arginfo=signature.get_argument(name),
        )
        used_keys.add(name)
    else:
        used_keys |= load_parameters(
            params.body, transmute_attrs.body_parameters, signature, transmute_attrs
        )

    # extract the parameters from the paths
    for name in _extract_path_parameters_from_paths(transmute_attrs.paths):
        params.path[name] = Param(
            argument_name=name,
            description=transmute_attrs.parameter_descriptions.get(name),
            arginfo=signature.get_argument(name),
        )
        used_keys.add(name)

    # check the method type, and decide if the parameters should be extracted
    # from query parameters or the body
    default_param_key = "query" if transmute_attrs.methods == set(["GET"]) else "body"
    default_params = getattr(params, default_param_key)

    # parse all positional params
    for arginfo in signature:
        if arginfo.name in used_keys:
            continue
        used_keys.add(arginfo.name)
        default_params[arginfo.name] = Param(
            arginfo.name,
            description=transmute_attrs.parameter_descriptions.get(arginfo.name),
            arginfo=arginfo,
        )

    return params


PART_REGEX = re.compile(r"(\{[_a-zA-Z][^{}]*(?:\{[^{}]*\}[^{}]*)*\})")
PARAM_REGEX = re.compile(r"^\{(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\}$")


def _extract_path_parameters_from_paths(paths):
    """
    from a list of paths, return back a list of the
    arguments present in those paths.

    the arguments available in all of the paths must match: if not,
    an exception will be raised.
    """
    params = set()
    for path in paths:
        parts = PART_REGEX.split(path)
        for p in parts:
            match = PARAM_REGEX.match(p)
            if match:
                params.add(match.group("name"))
    return params


def load_parameters(param_set, param_list, signature, transmute_attrs):
    used_keys = set()
    for name in param_list:
        param_set[name] = Param(
            argument_name=name,
            description=transmute_attrs.parameter_descriptions.get(name),
            arginfo=signature.get_argument(name),
        )
        used_keys.add(name)
    return used_keys
