from collections import namedtuple


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

    def get_argument(self, key):
        if key in self.kwargs:
            return self.kwargs[key]
        for arg in self.args:
            if arg.name == key:
                return arg

    @staticmethod
    def from_argspec(argspec):
        """
        retrieve a FunctionSignature object
        from the argspec and the annotations passed.
        """
        attributes = (getattr(argspec, "args", []) +
                      getattr(argspec, "keywords", []))
        defaults = argspec.defaults or []

        arguments, keywords = [], {}

        attribute_list = (attributes[:-len(defaults)]
                          if len(defaults) != 0
                          else attributes[:])
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
