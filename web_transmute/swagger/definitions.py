from .utils import SWAGGER_TYPEMAP


class Definitions(object):
    """
    this class handler returning the correct swagger type spec.
    it will handler returning the proper schema value.
    """

    def __init__(self):
        self._element_name = "definitions"
        self._definitions = ModelDict()

    def get(self, model_or_cls):
        if isinstance(model_or_cls, dict):
            return self._get_reference(model_or_cls)

        if isinstance(model_or_cls, list):
            return {
                "type": "array",
                "items": self.get(model_or_cls[0]),
                "collectionFormat": "multi"
            }

        for typ, typ_name in SWAGGER_TYPEMAP.items():
            if issubclass(model_or_cls, typ):
                return {"type": typ_name}

        return self._get_reference(model_or_cls)

    def add_to_spec(self, spec):
        """ add definitions to the swagger spec """
        spec[self._element_name] = self._definitions

    def _get_reference(self, model_or_cls):
        self.add_model(model_or_cls)

        reference = "#/{0}/{1}".format(
            self._element_name,
            self._definitions.to_id(model_or_cls)
        )
        return {"$ref": reference}

    def add_model(self, model_or_cls):
        if not isinstance(model_or_cls, dict):
            model = model_or_cls.transmute_schema
        else:
            model = model_or_cls

        schema = self._expand_schema(model)
        self._definitions[model_or_cls] = schema
        return schema

    def _expand_schema(self, schema):
        properties = {}
        for property_name, details in schema["properties"].items():
            properties[property_name] = self.get(details["type"])

        return {
            "type": "object",
            "properties": properties,
            "required": schema["required"]
        }


class ModelDict(dict):
    """
    a dictionary that accepts class names or dictionaries
    as a key.
    """
    def __init__(self, *args, **kwargs):
        # for dictionaries, a stringified key
        # won't work in the swagger spec.
        # instead, we assign them ids instead.
        self._ids = {}

    def __getitem__(self, key, value):
        key = self.to_id(key)
        return super(ModelDict, self).__getitem__(key, value)

    def __setitem__(self, key, value):
        key = self.to_id(key)
        return super(ModelDict, self).__setitem__(key, value)

    def __contains__(self, key):
        key = self.to_id(key)
        return super(ModelDict, self).__contains__(key)

    def to_id(self, key):
        if isinstance(key, dict):
            ids_key = str(key)
            if ids_key not in self._ids:
                model_key = str(len(self._ids))
                self._ids[ids_key] = model_key
                return model_key
            else:
                return self._ids[ids_key]
        elif isinstance(key, type):
            key = "{0}.{1}".format(key.__module__, key.__name__)
        return key
