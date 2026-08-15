import threading

from sqlite3 import Connection
from functools import lru_cache
from ..functional import partial_right


class SqliteStorage:
    
    def __init__(self, filepath:str, max_connection:int=32):
        self.filepath = filepath
        
        connection_initator = lru_cache(maxsize=max_connection)(_init_connection)
        connection_initator = partial_right(connection_initator, filepath)

    @property
    def connection(self):
        thread_id = threading.get_ident()
        return _init_connection(self.filepath, thread_id)
    
    def query(self, statement:str):
        return Query(self, statement)
    
    def execute(self, *statements:str):
        with self.connection as conn:
            for s in statements:
                conn.execute(s)
            

def _init_connection(filepath:str, thread_id:int):
    return Connection(filepath)


class Query:
    
    def __init__(self, storage:SqliteStorage, query:str):
        self.storage = storage
        self.query = query
    
    def executemany(self, params=None):
        params =  params or []
        with self.storage.connection as conn:
            conn.executemany(self.query, params)
    
    def execute(self, params=None):
        params = params or []
        with self.storage.connection as conn:
            yield from conn.execute(self.query, params)
    
    def __repr__(self):
        return self.query
