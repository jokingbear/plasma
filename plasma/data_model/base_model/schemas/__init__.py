from .accessors import AccessorSchema
from .struct import StructSchema
from .utils import struct2accessor, accessor2struct
from .base import Schema
from .realization import Realization
from .representation import GraphRepresetation
from ..constants import MODEL_FLAG


def schema(cls:type) -> Schema:
    return getattr(cls, MODEL_FLAG)
