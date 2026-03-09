from typing import get_args, get_origin

from .base2 import MODEL_FLAG
from ...functional import AutoPipe


class Validator[T](AutoPipe[[T], None]):
    
    def __init__(self, cls:type[T], context=None):
        super().__init__()
        assert hasattr(cls, MODEL_FLAG), 'only support data model validation'
        
        self.cls = cls
        self.context = context
    
    def run(self, object:T):
        exceptions = []
        for field_name, field_type in self.cls.__annotations__.items():
            field_value = getattr(object, field_name)
            
            if self.context is not None:
                field_name = f'{self.context}.{field_name}'
            
            if field_value is None:
                continue
            
            if _is_list(field_type):
                _validate_instance(field_name, (tuple, list), field_value)
                
                origin = get_origin(field_type)
                if origin is not None:
                    field_type, *_ = get_args(field_type)

                for i, v in enumerate(field_value):
                    new_field_name = f'{field_name}[{i}]'
                    try:
                        _validate_instance(new_field_name, field_type, v)
                        
                        if hasattr(field_type, MODEL_FLAG):
                            Validator(field_type, new_field_name)(v)
                    except TypeError as e:
                        exceptions.append(e)
            else:
                try:
                    _validate_instance(field_name, field_type, field_value)
                    
                    if hasattr(field_type, MODEL_FLAG):
                        Validator(field_type, field_name)(field_value)
                except TypeError as e:
                    exceptions.append(e)
            
            if len(exceptions) > 0:
                raise TypeError(*[str(e) for e in exceptions])


def _is_list(cls:type):
    origin = get_origin(cls)
    return origin is not None and issubclass(origin, (tuple, list)) \
            or origin is None and issubclass(cls, (tuple, list)) 


def _validate_instance(field_name, cls, obj):
    if not isinstance(obj, cls):
        raise TypeError(f'{obj} is not instance of {cls} at field {field_name}')
