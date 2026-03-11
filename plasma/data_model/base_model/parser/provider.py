from typing import Callable

from .base import Parser
from ....functional import AutoPipe


class ParsingProvider(AutoPipe):
    
    def __init__(self):
        super().__init__()
        
        self.type_parser = dict[type, Callable[[object], object]]()
    
    def run[T](self, cls:type[T]):
        return Parser[T](cls, self.type_parser)

    def register[T](self, cls:type[T], parser:Callable[[object], T]):
        self.type_parser[cls] = parser
        return self
