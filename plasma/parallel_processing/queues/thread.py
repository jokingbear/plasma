import threading
import queue

from .signals import Signal
from .utils import internal_run
from .base import Queue


class ThreadQueue(Queue[list[threading.Thread]]):

    def __init__(self, n=1, name=None, qsize=0, timeout=None):
        super().__init__(name, n)

        self._queue = queue.Queue(qsize)
        self.timeout = timeout

    def _init_state(self):
        if self._callback is None:
            raise AttributeError('there is no registered callback for this queue.')
        
        threads = [threading.Thread(target=internal_run, args=(self._queue, self._callback, self._exception_handler)) 
                   for i in range(self.num_runner)]
        [t.start() for t in threads]
        return threads

    def _put(self, x):
        self._queue.put(x, block=True, timeout=self.timeout)
    
    def release(self):
        self._queue.join()
        if self._state is not None:
            for _ in self._state:
                self._queue.put(Signal.CANCEL)
            self._queue.join()

            for t in self._state:
                t.join()

        old_queue = self._queue
        old_queue.shutdown()
        
        new_queue = queue.Queue(old_queue.maxsize)
        self._queue = new_queue
        del old_queue

        super().release()

    def is_alive(self):
        return (
            self.running 
            and self._state is not None
            and any(t.is_alive() for t in self._state)
        )
    
    def __getstate__(self):
        state:dict = super().__getstate__() #type:ignore - dict like
        state = state.copy()
        state['qsize'] = self._queue.maxsize
        state['_state'] = None 
        state['_queue'] = None 
        return state

    def __setstate__(self, state:dict):
        state['_queue'] = queue.Queue(state.pop('qsize'))
        self.__dict__.update(state)
