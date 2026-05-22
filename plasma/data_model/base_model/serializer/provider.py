from typing import Callable, Any
from .base import Serializer


class SerializationProvider:
    
    def __init__(self):
        super().__init__()
        
        self.type_serializer = dict[type, Callable[[Any], Any]]()
    
    def run[T](self, cls:type[T], expand_none=False):
        return Serializer[T](cls, self.type_serializer, expand_none)
    
    def __call__[T](self, cls:type[T], expand_none=False):
        return self.run(cls, expand_none)

    def register[T](self, cls:type[T], serializer:Callable[[T], object]):
        self.type_serializer[cls] = serializer
        return self
