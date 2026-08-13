import threading

from sqlite3 import Connection
from functools import lru_cache
from ..functional import partial_right


class SqliteStorage:
    
    def __init__(self, filepath:str, max_connection:int=32):
        self.filepath = filepath
        
        connection_initator = lru_cache(maxsize=max_connection)(_init_connection)
        connection_initator = partial_right(connection_initator, filepath)
        self._init_connection = connection_initator

    @property
    def connection(self):
        thread_id = threading.get_ident()
        return self._init_connection(thread_id)
    
    def query(self, statement:str):
        return Query(self, statement)


def _init_connection(filepath:str, thread_id:int):
    return Connection(filepath)


class Query:
    
    def __init__(self, storage:SqliteStorage, query:str):
        self.storage = storage
        self.query = query
    
    def executemany(self, params):
        with self.storage.connection as conn:
            conn.executemany(self.query, params)
    
    def execute(self, params):
        with self.storage.connection as conn:
            return conn.execute(self.query, params)
    
    def __repr__(self):
        return self.query
