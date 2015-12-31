from ..compat import string_type

SWAGGER_TYPEMAP = {
    string_type: "string",
    int: "integer",
    bool: "boolean",
    list: "array",
    type(None): "null"
}
