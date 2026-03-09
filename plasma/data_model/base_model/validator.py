from logging import exception
from typing import get_args, get_origin

from .base2 import MODEL_FLAG
from ...functional import AutoPipe


class Validator[T](AutoPipe[[T], None]):
    
    def __init__(self, cls:type[T]):
        super().__init__()
        assert hasattr(cls, MODEL_FLAG), 'only support data model validation'
        
        self.cls = cls
    
    def run(self, object:T):
        exceptions = [*_validate_object(None, self.cls, object)]
            
        if len(exceptions) > 0:
            messages = [e.args[0] for e in exceptions]
            fields = [e.args[1] for e in exceptions]
            
            error = TypeError(fields)
            error.add_note('\n'.join(messages))
            raise error


def _validate_object(context, field_type:type, obj):
    exception = _validate_instance(context, field_type, obj)
    
    if exception is not None:
        yield exception
    elif hasattr(field_type, MODEL_FLAG):
        for field_name, field_type in field_type.__annotations__.items():
            field_value = getattr(obj, field_name)
            field_name = field_name if context is None else f'{context}.{field_name}'
            
            if _is_list(field_type):
                iterator = _validate_list(field_name, field_type, field_value)
            else:
                iterator = _validate_object(field_name, field_type, field_value)

            for e in iterator:
                yield e


def _is_list(cls:type):
    origin = get_origin(cls)
    return origin is not None and issubclass(origin, (tuple, list)) \
            or origin is None and issubclass(cls, (tuple, list)) 


def _validate_list(field_name, field_type, field_value):
    exception = _validate_instance(field_name, (tuple, list), field_value)
    
    if exception is not None:
        yield exception

    else:
        origin = get_origin(field_type)
        if origin is not None:
            field_type, *_ = get_args(field_type)

        for i, v in enumerate(field_value):
            new_field_name = f'{field_name}[{i}]'
            for e in _validate_object(new_field_name, field_type, v):
                yield e


def _validate_instance(field_name, cls, obj):
    if not isinstance(obj, cls):
        msg = f'{obj} is not instance of {cls}'
        if field_name is not None:
            msg += f'at field {field_name}'

        return TypeError(msg, field_name)
