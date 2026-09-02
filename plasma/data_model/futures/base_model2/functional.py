from dataclasses import dataclass
from typing import dataclass_transform

from .arch import SCHEMA_FIELD, is_model
from .schemas.base import Schema


@dataclass_transform()
def model(t:type):
    setattr(t, SCHEMA_FIELD, None)
    setattr(t, SCHEMA_FIELD, Schema(t))
    return dataclass(t, slots=True)


def schema(t:type) -> Schema:
    assert is_model(t), f'{t} is not a model'
    return getattr(t, SCHEMA_FIELD)
