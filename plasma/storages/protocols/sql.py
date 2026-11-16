from collections.abc import Sequence, Iterable
from typing import Protocol, Any


class SQLDriver[C:Connector](Protocol):
    
    @property
    def connector(self) -> C:...
    
    def statement(self, contents:str) -> Statement[C]:...
    
    def execute(self, *statements:Statement[C]):
        with self.connector as conn:
            supports = statements[:-1]
            main = statements[-1]
            for s in supports:
                s.execute(conn)
            return [*main.execute(conn)]


class Statement[C](Protocol):
    text:str
    params:Sequence
    kwarg_params:dict[str, Any]
    dml:bool
    execute_many:bool
    
    def parameterize(self, 
        *params, dml:bool=False, 
        execute_many:bool=False, 
        **kwargs
    ) -> Statement[C]:...
    
    def execute(self, connector:C) -> Iterable: ...


class Connector(Protocol):
    
    def __enter__(self) -> Any:...
    
    def __exit__(self, exc_type, exc, tb):...
