import zmq

from .publisher import PubZMQ
from .consumer import SubZMQ
from ....serializers import Serializer, Pickler


class ZContext:
    
    def __init__(self):
        self._context = zmq.Context()
    
    def publisher(self, 
            connection:str, name:str|None=None, 
            qsize:int=0, timeout:float=0, 
            serializer:Serializer|None=None
        ):
        return PubZMQ(
            self._context, connection, name,
            qsize, timeout, serializer or Pickler()
        )
    
    def consumer(self,
            connection:str, name:str|None=None, 
            n:int=1, prefetch:int=1, serializer:Serializer|None=None
        ):
        return SubZMQ(
            self._context, connection, name,
            n, prefetch, serializer or Pickler()
        )