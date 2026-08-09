import threading

from sqlite3 import Connection
from functools import lru_cache


class SqliteStorage:
    
    def __init__(self, filepath:str, max_connection:int=32):
        self.filepath = filepath
        self._init_connection = lru_cache(maxsize=max_connection)(
            self._init_connection, 
        )

    @property
    def connection(self):
        thread_id = threading.get_ident()
        return self._init_connection(thread_id)
    
    def _init_connection(self, thread_id):
        return Connection(self.filepath)
