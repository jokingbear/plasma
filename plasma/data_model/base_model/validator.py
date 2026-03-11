import re

from typing import get_args, get_origin
from enum import Enum

from .inquirer import is_data_model
from .schemas import AccessorSchema
from .field import Field, List
from .serializer import Serializer
from ...functional import AutoPipe


class Validator[T](AutoPipe[[T], None]):
    
    def __init__(self, cls:type[T]):
        super().__init__()
        assert is_data_model(cls), 'only support data model validation'
        
        self.cls = cls
        self._serializer = Serializer(cls, {})
        self._schema = AccessorSchema(cls)
    
    def run(self, object:T):
        accessors = self._serializer.to_accessors(object)
        notes = []
        fields = []
        for a, v in accessors.items():
            schema_key = a
            if re.search(r'\.\d+', a) is not None:
                schema_key = re.sub(r'\.\d+', '.@idx', a)
           
            if schema_key not in self._schema:
                notes.append(f'field {a} with value {v} does not conform to schema of {self.cls}')
                fields.append(a)
                continue

            schema_field = self._schema[schema_key]
            if isinstance(schema_field, List):
                invalid_notes = [*_validate_list(schema_field.cls, v)]
                if len(invalid_notes) > 0:
                    fields.append(a)
                    notes.extend(invalid_notes)
            else:
                invalid_note = _validate_object(schema_field.cls, v)
                if invalid_note is not None:
                    notes.append(invalid_note)
                    fields.append(a)
        
        if len(fields) > 0:
            error = AttributeError(fields)
            for n in notes:
                error.add_note(n)

            raise AttributeError(fields)


def _validate_object(field_type:type, obj):
    if isinstance(field_type, type) and issubclass(field_type, Enum) and not isinstance(obj, Enum):
        return f'{obj} is not of enum {field_type}'
    elif not isinstance(obj, field_type):
        return f'{obj} is not of instance {field_type}'


def _validate_list(field_type, field_value):    
    if not isinstance(field_value, (tuple, list)):
        yield f'{field_value} is not a list or tuple'
    elif field_type is not None:
        for v in field_value:
            invalid_note = _validate_object(field_type, v)
            if invalid_note is not None:
                yield _validate_object(field_type, v)
