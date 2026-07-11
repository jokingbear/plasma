import zmq
import threading

from typing import Sequence, Callable, Any
from ..base import Queue
from ..signals import Signal
from ....serializers import Serializer, Pickler


class SubZMQ(Queue[Sequence[threading.Thread]]):
    
    def __init__(self, 
            connection:str, name=None, 
            num_runner=1, serializer:Serializer=Pickler(),
        ):
        super().__init__(name, num_runner)
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(connection)
        
        self.connection = connection
        self._socket = socket
        self.serializer = serializer
    
    def _put(self, x):
        raise NotImplementedError('consumer queue cannot be put')
    
    def _init_state(self):
        threads = []
        args = [
            self._socket, self.serializer,
            self._callback, self._exception_handler
        ]
        for _ in range(self.num_runner):
            thread = threading.Thread(target=_run, args=args)
            thread.start()
            threads.append(thread)

        return threads
    
    
def _run(
        socket:zmq.Socket,
        serializer:Serializer,
        processor:Callable[..., None], 
        exception_handler:Callable[[Any, Exception], None]
    ):
    while True:
        data = serializer.deserialize(socket.recv())
        
        try:
            if data is Signal.CANCEL:
                break
            
            processor(data)
        except Exception as e:
            if exception_handler is None:
                raise e

            exception_handler(data, e)
