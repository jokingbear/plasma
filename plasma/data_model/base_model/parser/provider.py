from typing import Callable, Any
from warnings import deprecated

from .base import Parser


class ParsingProvider:
    
    def __init__(self):
        super().__init__()
        
        self._sub_parsers = dict[type, Callable[[object], object]]()
    
    def to[T](self, cls:type[T]):
        return Parser[T](cls, self._sub_parsers)

    @deprecated('use provider.to instead')
    def run[T](self, cls:type[T]):
        return Parser[T](cls, self._sub_parsers)

    def register[T](self, cls:type[T], parser:Callable[[Any], T|None]):
        self._sub_parsers[cls] = parser
        return self
