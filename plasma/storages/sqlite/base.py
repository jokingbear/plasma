import threading

from sqlite3 import Connection
from functools import lru_cache

from .statement import SqliteStatement
from ..protocols import SQLDriver


class SqliteStorage(SQLDriver[Connection, SqliteStatement]): # type: ignore
    
    def __init__(self, filepath:str, max_connection:int=32):
        self.filepath = filepath
        
        connection_initator = lru_cache(maxsize=max_connection)(_init_connection)
        self._connection_initiator = connection_initator

    @property
    def connector(self):
        thread_id = threading.get_ident()
        return self._connection_initiator(self.filepath, thread_id)
    
    def statement(self, contents:str):
        return SqliteStatement(contents, [])


def _init_connection(filepath:str, thread_id:int):
    return Connection(filepath)
