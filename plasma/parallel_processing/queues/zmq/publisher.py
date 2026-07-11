import zmq
import threading

from queue import Full
from ..base import Queue
from ....serializers import Serializer, Pickler


class PubZMQ(Queue):
    
    def __init__(self, 
            connection:str, name:str|None=None, 
            qsize:int=10, timeout:float=0,
            serializer:Serializer|None=None,
        ):
        super().__init__(name, 0)        
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        
        if qsize > 0:
            socket.setsockopt(zmq.SNDHWM, qsize)
        
        if timeout > 0:
            socket.setsockopt(zmq.SNDTIMEO, int(timeout * 1000))

        socket.connect(connection)
        self._socket = socket
        self.qsize = qsize
        self.serializer = serializer or Pickler()
        self._lock = threading.Lock()
    
    def _put(self, x):
        contents = self.serializer.serialize(x)
        with self._lock:
            try:
                self._socket.send(contents, copy=False)
            except zmq.Again as e:
                raise Full() from e
    
    def run(self):
        raise NotImplementedError('publisher queue cannot be run')

    def release(self):
        self._socket.close()
        return super().release()
