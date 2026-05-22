from typing import Sequence, get_origin, get_args, Union, Optional
from .utils import is_data_model
from .schemas import schema
from ...functional import ReadableClass


class Validator[T](ReadableClass):
    
    def __init__(self, cls:type[T], strict=True):
        super().__init__()
        assert is_data_model(cls), 'only support data model validation'
        
        self.cls = cls
        self._schema = schema(cls)
        self.strict = strict
    
    def __call__(self, object:T):
        realization = self._schema.realize(object)
        error_fields = []
        notes = []
        for e in realization.endpoints:
            value = realization.value(e)
            rep = self._schema.real_to_rep(e)
            raw = self._schema.rep.raw(rep)
            origin, args = self._schema.rep.type(rep)
            
            field_name = '.'.join(str(a) for a in e)
            if issubclass(origin, tuple|list):
                enotes = [*self._validate_list(field_name, args, value)]
                if len(enotes) > 0:
                    error_fields.append(field_name)
                    notes.extend(enotes)
            else:
                enotes = self._validate_object(field_name, value, raw, origin, args)
                if enotes is not None:
                    error_fields.append(field_name)
                    notes.append(enotes)
        
        if len(error_fields) > 0:
            error = TypeError(*error_fields)
            for n in notes:
                error.add_note(n)
            raise error

    def _validate_object(self, field_name, obj, raw, origin, args):
        valid_condition = (
            isinstance(obj, origin) or 
            (len(args) > 0 and isinstance(obj, args))
        )
        valid_condition |= obj is None and not self.strict
        
        if not valid_condition:
            types = [origin, *args]
            return f'{obj} is not of instance {raw} at field {field_name}'

    def _validate_list(self, field_name, args, field_value):    
        if not isinstance(field_value, Sequence):
            yield f'{field_value} is not a list or tuple at {field_name}'
        elif len(args) > 0:
            origin = get_origin(args[0])
            generic_args = get_args(args[0])
            for i, v in enumerate(field_value):
                invalid_note = self._validate_object(f'{field_name}.{i}', v, args[0], origin, generic_args)
                if invalid_note is not None:
                    yield invalid_note
