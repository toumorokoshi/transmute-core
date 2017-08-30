class Template(object):
    """
    a rudimentary replacement for Jinja2. currently in place
    due to a bug with  the typing module.
    """

    def __init__(self, template_string):
        self._template_string = template_string

    def render(self, **parameters):
        chunks = []
        iterator = iter(self._template_string)
        while True:
            try:
                c = next(iterator)
                if c == "{":
                    next_c = next(iterator)
                    if next_c == "{":
                        chunks.append(_capture_variable(iterator, parameters))
                    else:
                        chunks.append(c)
                        chunks.append(next_c)
                    continue
                chunks.append(c)
            except StopIteration:
                break
        return "".join(chunks)


def _capture_variable(iterator, parameters):
    """
    return the replacement string.
    this assumes the preceeding {{ has already been
    popped off.
    """
    key = ""
    next_c = next(iterator)
    while next_c != "}":
        key += next_c
        next_c = next(iterator)
    # remove the final "}"
    next(iterator)
    return parameters[key]
