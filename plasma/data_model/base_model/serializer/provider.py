from typing import Callable

from .base import Serializer
from ....functional import AutoPipe


class SerializationProvider(AutoPipe):
    
    def __init__(self):
        super().__init__()
        
        self._type_serializer = dict[type, Callable[[object], object]]()
    
    def run[T](self, cls:type[T]):
        return Serializer[T](cls, self._type_serializer)

    def register[T](self, cls:T, serializer:Callable[[T], object]):
        self.type_serializer[cls] = serializer
        return self
