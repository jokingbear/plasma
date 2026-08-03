import zmq
import threading

from dataclasses import dataclass
from ..base import Queue
from ..signals import Signal
from ..thread import ThreadQueue
from ....serializers import Serializer, Pickler


class SubZMQ(Queue["_State"]):
    
    def __init__(self, 
            connection:str, name=None, 
            n=1, prefetch=1,
            serializer:Serializer|None=None,
        ):
        super().__init__(name, n)

        self.prefetch = prefetch
        self.connection = connection
        self.serializer = serializer or Pickler()
    
    def _put(self, x):
        raise NotImplementedError('consumer queue cannot be put')
    
    def _init_state(self):
        return _State(
            zmq.Context(), self.connection,
            self.serializer,
            ThreadQueue(n=self.num_runner, qsize=self.prefetch)
                .register_callback(self._callback)
                .on_exception(self._exception_handler) # type:ignore
                .run()
        ).start()
    
    def release(self):
        if self._state is not None:
            self._state.release()

        return super().release()


@dataclass
class _State:
    context:zmq.Context
    connection:str
    serializer:Serializer
    workers: ThreadQueue
    
    def start(self):
        threading.Thread(target=self._run).start()
        return self
    
    def _run(self):
        socket:zmq.Socket = self.context.socket(zmq.PULL)
        socket.bind(self.connection)
        
        while True:
            data = self.serializer.deserialize(socket.recv())
            if data is Signal.CANCEL:
                break

            self.workers.put(data)
        
        socket.close(0)
        
    def release(self):
        socket = self.context.socket(zmq.PUSH)
        socket.connect(self.connection)
        socket.send(
            self.serializer.serialize(Signal.CANCEL)
        )
        self.workers.release()
