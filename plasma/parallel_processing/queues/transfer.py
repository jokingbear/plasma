from multiprocessing import JoinableQueue
from threading import Thread
from typing import Sequence

from .base import Queue
from .signals import Signal
from .utils import internal_run
from ...functional import partials


class TransferQueue(Queue[Sequence[Thread]]):

    def __init__(self, name=None, n=1, qsize=0):
        super().__init__(name, n)

        self._receiver = JoinableQueue(qsize)
        self._qsize = qsize

    def _put(self, x):
        self._receiver.put(x, block=True)

    def _init_state(self):
        runner = partials(internal_run, self._receiver, self._callback, self._exception_handler)
        threads = [Thread(target=runner)  for _ in range(self.num_runner)]
        [t.start() for t in threads]
        return threads

    def release(self):
        assert self._state is not None, 'queue has not been run'
        for t in self._state:
            self._receiver.put(Signal.CANCEL)
        
        for t in self._state:
            t.join()

        old_queue = self._receiver
        old_queue.close()
        
        new_queue = JoinableQueue(self._qsize)
        self._receiver = new_queue
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
        state['_state'] = None 
        return state
