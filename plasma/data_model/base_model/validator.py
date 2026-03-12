from enum import Enum

from .inquirer import is_data_model
from .schemas import schema
from ...functional import AutoPipe


class Validator[T](AutoPipe[[T], None]):
    
    def __init__(self, cls:type[T]):
        super().__init__()
        assert is_data_model(cls), 'only support data model validation'
        
        self.cls = cls
        self._schema = schema(cls)
    
    def run(self, object:T):
        realization = self._schema.realize(object)
        error_fields = []
        notes = []
        for e in realization.endpoints:
            value = realization.value(e)
            rep = self._schema.real_to_rep(e)
            origin, args = self._schema.rep.type(rep)
            
            field_name = '.'.join(str(a) for a in e)
            if issubclass(origin, (tuple, list)):
                enotes = [*_validate_list(field_name, args, value)]
                error_fields.append(field_name)
                notes.extend(enotes)
            else:
                enotes = _validate_object(field_name, origin, value)
                if enotes is not None:
                    error_fields.append(field_name)
                    notes.append(enotes)
        
        if len(error_fields) > 0:
            error = AttributeError(*error_fields)
            for n in notes:
                error.add_note(n)
            raise error


def _validate_object(field_name, field_type:type, obj):
    if obj is not None and not isinstance(obj, field_type):
        return f'{obj} is not of instance {field_type} at field {field_name}'


def _validate_list(field_name, args, field_value):    
    if not isinstance(field_value, (tuple, list)):
        yield f'{field_value} is not a list or tuple at {field_name}'
    elif len(args) > 0:
        for i, v in enumerate(field_value):
            invalid_note = _validate_object(f'{field_name} item {i}', args[0], v)
            if invalid_note is not None:
                yield invalid_note
