from cattr import Converter
from ...compat import string_type
from schematics.models import Model

def create_cattrs_converter():
    converter = Converter()
    converter.register_structure_hook(bool, _structure_bool)
    converter.register_structure_hook(string_type, _structure_string)
    converter.register_structure_hook(Model, _structure_schematics)
    converter.register_unstructure_hook(Model, _unstructure_schematics)
    return converter


def _structure_bool(data, cls):
    if isinstance(data, bool):
        return data
    return str(data).lower().startswith("t")


def _structure_string(data, cls):
    return str(data)


def _structure_schematics(data, cls):
    return cls(data)

def _unstructure_schematics(data):
    return data.to_primitive()
