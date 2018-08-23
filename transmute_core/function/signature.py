import attr


class NoDefault(object):
    def __str__(self):
        return "NoDefault"

    def __repr__(self):
        return "NoDefault"


NoDefault = NoDefault()


@attr.s
class Argument(object):
    name = attr.ib()
    default = attr.ib()
    type = attr.ib()


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
        attributes = getattr(argspec, "args", []) + getattr(argspec, "keywords", [])
        defaults = argspec.defaults or []

        arguments, keywords = [], {}

        attribute_list = (
            attributes[: -len(defaults)] if len(defaults) != 0 else attributes[:]
        )
        for name in attribute_list:
            if name == "self":
                continue
            typ = argspec.annotations.get(name)
            arguments.append(Argument(name, NoDefault, typ))

        if len(defaults) != 0:
            for name, default in zip(attributes[-len(defaults) :], defaults):
                typ = argspec.annotations.get(name)
                keywords[name] = Argument(name, default, typ)

        return FunctionSignature(arguments, keywords)

    def __iter__(self):
        for arg in self.args:
            yield arg
        for kwarg in self.kwargs.values():
            yield kwarg

    def split_args(self, arg_dict):
        """
        given a dictionary of arguments, split them into
        args and kwargs

        note: this destroys the arg_dict passed. if you need it,
        create a copy first.
        """
        pos_args = []
        for arg in self.args:
            pos_args.append(arg_dict[arg.name])
            del arg_dict[arg.name]
        return pos_args, arg_dict
