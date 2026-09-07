import zmq
import threading

from queue import Full
from ..base import Queue
from ....serializers import Serializer


class PubZMQ(Queue):
    
    def __init__(self,
            context:zmq.Context, connection:str, name:str|None, 
            qsize:int, timeout:float,
            serializer:Serializer,
        ):
        super().__init__(name, 0)        

        socket:zmq.Socket = context.socket(zmq.PUSH)
        if qsize > 0:
            socket.setsockopt(zmq.SNDHWM, qsize)
        
        if timeout > 0:
            socket.setsockopt(zmq.SNDTIMEO, int(timeout * 1000))
        
        if 'tcp' in connection:
            socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
            socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 600)  # Pulse at 10 mins (Docker cuts at 15)
            socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 30)  # Retry every 30s if quiet
            socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 3)   
        
        socket.connect(connection)
        self._socket = socket
        self.qsize = qsize
        self.serializer = serializer
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
