# from .cattrs_extended_converter import ExtendedConverter
from cattr import Converter
from datetime import datetime
from ...compat import string_type
from schematics.models import Model
from schematics.types import DateTimeType, BaseType
from schematics.exceptions import BaseError


def create_cattrs_converter():
    converter = Converter()
    converter.register_structure_hook(bool, _structure_bool)
    converter.register_structure_hook(string_type, _structure_string)
    converter.register_structure_hook(Model, _structure_schematics)
    converter.register_structure_hook(BaseType, _structure_basetype)
    converter.register_structure_hook(datetime, _structure_datetime)
    converter.register_unstructure_hook(Model, _unstructure_schematics)
    converter.register_unstructure_hook(datetime, _unstructure_datetime)
    converter.register_unstructure_hook(BaseType, _unstructure_basetype)
    return converter


def _structure_bool(data, cls):
    if isinstance(data, bool):
        return data
    return str(data).lower().startswith("t")


def _structure_string(data, cls):
    return str(data)


def _structure_schematics(data, cls):
    value = cls(data)
    try:
        value.validate()
        return value
    except BaseError as de:
        raise ValueError(str(de))


def _unstructure_schematics(data):
    return data.to_primitive()


datetime_type = DateTimeType()


def _structure_datetime(data, cls):
    if not data:
        raise ValueError("datetime is empty")
    return datetime_type.to_native(data)


def _unstructure_datetime(data):
    return data.isoformat()


def _structure_basetype(data, cls):
    return data


def _unstructure_basetype(data, cls):
    return cls().to_primitive(data)
