from collections import namedtuple
from .compat import getfullargspec

Parameters = namedtuple("Parameters", ["query", "body", "header", "path"])


def get_parameters(func):
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
    argspec = getfullargspec(func)

    # exam


def get_signature(argspec):
    """
    retrieve a FunctionSignature object
    from the argspec and the annotations passed.
    """
    attributes = (getattr(argspec, "args", []) +
                  getattr(argspec, "keywords", []))
    defaults = argspec.defaults or []

    arguments, keywords = [], {}

    attribute_list = attributes[:-len(defaults)] if len(defaults) != 0 else attributes[:]
    for name in attribute_list:
        if name == "self":
            continue
        typ = argspec.annotations.get(name)
        arguments.append(Argument(name, NoDefault, typ))

    if len(defaults) != 0:
        for name, default in zip(attributes[-len(defaults):], defaults):
            typ = argspec.annotations.get(name)
            keywords[name] = Argument(name, default, typ)

    return FunctionSignature(arguments, keywords)


class NoDefault(object):

    def __str__(self):
        return "NoDefault"

    def __repr__(self):
        return "NoDefault"

NoDefault = NoDefault()


Argument = namedtuple("Argument", ["name", "default", "type"])


class FunctionSignature(object):

    NoDefault = NoDefault

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
