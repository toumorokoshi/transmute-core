import tornado.web

METHODS = ["get", "head", "post", "delete", "patch", "put", "options"]


def url_spec(transmute_path, handler, *args, **kwargs):
    """
    convert the transmute_path
    to a tornado compatible regex,
    and return a tornado url object.
    """
    p = _to_tornado_pattern(transmute_path)
    for m in METHODS:
        method = getattr(handler, m)
        if hasattr(method, "transmute_func"):
            method.transmute_func.paths.add(transmute_path)
    return tornado.web.URLSpec(p, handler, *args, **kwargs)


def _to_tornado_pattern(transmute_path):
    """convert a transmute path to
    a tornado pattern.
    """
    return (
        transmute_path.replace("{", "(?P<")
        # .replace("}", ">[^\/]+)"))
        .replace("}", ">.*)")
    )
