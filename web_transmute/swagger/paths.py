from ..function import NoDefault


class Paths(object):

    def __init__(self, definitions):
        self._paths = {}
        # this is a Definitions object.
        self._definitions = definitions

    def extract_from_app(self, app):
        for rule in app.url_map.iter_rules():
            path = rule.rule
            endpoint = rule.endpoint
            func = app.view_functions[endpoint]
            if hasattr(func, "transmute_func"):
                if path not in self._paths:
                    self._paths[path] = {}

                self._paths[path].update(
                    self._extract_swagger_pathspec(func.transmute_func)
                )

    def add_to_spec(self, spec):
        spec["paths"] = self._paths

    def _extract_swagger_pathspec(self, transmute_func):
        path_spec = {
            "description": transmute_func.description,
            "produces": transmute_func.produces,
            "parameters": [],
            "responses": {}
        }

        if transmute_func.updates or transmute_func.creates:
            # in the case of updates or creates, we spec this by
            # specifying all values are passed into the body.
            param_spec = {"name": "body", "in": "body", "required": True}
            properties = {}
            required = []
            for arg_name, arg_info in transmute_func.arguments.items():
                properties[arg_name] = {"type": arg_info.type}
                if arg_info.default is NoDefault:
                    required.append(arg_name)
            model = {"properties": properties, "required": required}
            param_spec["schema"] = self._definitions.get(model)
            path_spec["parameters"].append(param_spec)

        else:
            for arg_name, arg_info in transmute_func.arguments.items():
                param_spec = {
                    "name": arg_name,
                    "required": arg_info.default is not None,
                    "in": "query"
                }
                type_definition = self._definitions.get(arg_info.type)
                param_spec.update(type_definition)

                path_spec["parameters"].append(param_spec)

        for code, details in transmute_func.responses.items():
            response_spec = {"description": details["description"]}
            if details["return_type"] is not type(None):
                response_spec["schema"] = self._definitions.get(details["return_type"])
            path_spec["responses"][str(code)] = response_spec

        method = "get"
        if transmute_func.creates:
            method = "put"
        elif transmute_func.updates:
            method = "post"
        elif transmute_func.deletes:
            method = "delete"
        return {method: path_spec}
