import zmq
import threading

from typing import Sequence, Callable, Any
from ..base import Queue
from ..signals import Signal
from ....serializers import Serializer, Pickler


class SubZMQ(Queue[Sequence[threading.Thread]]):
    
    def __init__(self, 
            connection:str, name=None, 
            n=1, serializer:Serializer=Pickler(),
        ):
        super().__init__(name, n)
        context = zmq.Context()        
        self._context = context
        self.connection = connection
        self.serializer = serializer
    
    def _put(self, x):
        raise NotImplementedError('consumer queue cannot be put')
    
    def _init_state(self):
        threads = []
        args = [
            self._context, self.connection, self.serializer,
            self._callback, self._exception_handler
        ]
        for _ in range(self.num_runner):
            thread = threading.Thread(target=_run, args=args)
            thread.start()
            threads.append(thread)

        return threads
    
    def release(self):
        return super().release()


def _run(
        context:zmq.Context, connection:str,
        serializer:Serializer,
        processor:Callable[..., None], 
        exception_handler:Callable[[Any, Exception], None]
    ):
    socket = context.socket(zmq.PULL)
    socket.connect(connection)
    # socket.setsockopt(zmq.SUBSCRIBE, b"")
    
    try:
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
    finally:
        socket.close()
