import threading

from sqlite3 import Connection
from functools import lru_cache
from .statement import Statement


class SqlStorage:
    
    def __init__(self, filepath:str, max_connection:int=32):
        self.filepath = filepath
        
        connection_initator = lru_cache(maxsize=max_connection)(_init_connection)
        self._connection_initiator = connection_initator

    @property
    def connection(self):
        thread_id = threading.get_ident()
        return self._connection_initiator(self.filepath, thread_id)
    
    def statement(self, text:str):
        return Statement(text, [], False)
    
    def execute(self, *statements:Statement):
        with self.connection as conn:
            supports = statements[:-1]
            main = statements[-1]
            for s in supports:
                s.execute(conn)
            return [*main.execute(conn)]


def _init_connection(filepath:str, thread_id:int):
    return Connection(filepath)
