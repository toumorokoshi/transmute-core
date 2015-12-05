from collections import namedtuple


def get_signature(argspec):
    """
    retrieve a FunctionSignature object
    from the argspec and the annotations passed.
    """
    attributes = (getattr(argspec, "args", []) +
                  getattr(argspec, "keywords", []))
    defaults = argspec.defaults or []

    arguments, keywords = [], {}

    for name in attributes[:-len(defaults)]:
        if name == "self":
            continue
        typ = argspec.annotations.get(name)
        arguments.append(Argument(name, NoDefault, typ))

    start_index = len(defaults) + 1 or
    for name, default in zip(attributes[len(defaults):], defaults):
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

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
