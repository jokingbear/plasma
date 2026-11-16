from collections.abc import Sequence, Iterable
from typing import Protocol, Any, Self


class SQLDriver[C:Connector, S:SqlStatement](Protocol):
    
    @property
    def connector(self) -> C:...
    
    def statement(self, contents:str) -> S:...
    
    def execute(self, *statements:S):
        with self.connector as conn:
            supports = statements[:-1]
            main = statements[-1]
            for s in supports:
                s.execute(conn)
            return [*main.execute(conn)]


class SqlStatement[C](Protocol):
    text:str
    args:Sequence | dict[str,Any]
    execute_many:bool
    
    @property
    def dml(self) -> bool:...
    
    def parameterize(self, 
        *args, execute_many:bool|None=None, 
        **kwargs
    ) -> Self:...
    
    def execute(self, connector:C) -> Iterable: ...


class Connector(Protocol):
    
    def __enter__(self) -> Any:...
    
    def __exit__(self, exc_type, exc, tb):...
