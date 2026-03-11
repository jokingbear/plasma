from typing import Callable

from .base import Parser
from ....functional import AutoPipe


class ParsingProvider(AutoPipe):
    
    def __init__(self):
        super().__init__()
        
        self._type_serializer = dict[type, Callable[[object], object]]()
    
    def run[T](self, cls:type[T]):
        return Parser[T](cls, self._type_serializer)
