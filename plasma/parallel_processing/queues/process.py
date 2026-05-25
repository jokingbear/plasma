import multiprocessing as mp
import threading

from typing import Sequence, NamedTuple, Callable, Any
from .signals import Signal
from .utils import internal_run
from .base import Queue
from ...functional import partial_left
from ...logging import TraceableException


class _State(NamedTuple):
    processes:Sequence[mp.Process]
    error_queue:mp.JoinableQueue
    error_catcher:threading.Thread
    
    def run(self):
        for p in self.processes:
            p.start()
        
        self.error_catcher.start()
    
    def release(self):
        for p in self.processes:
            p.join()
            p.terminate()
        
        self.error_queue.put(Signal.CANCEL)
        self.error_catcher.join()
        self.error_queue.close()
    

class ProcessQueue(Queue[_State]):

    def __init__(self, n=1, name=None, qsize=0, timeout=None):
        super().__init__(name, n)

        self._queue = mp.JoinableQueue(qsize)
        self.timeout = timeout
        self._qsize = qsize

    def _init_state(self):
        error_queue = mp.JoinableQueue()
        state = _State(
            [
                mp.Process(
                    target=internal_run, 
                    args=(
                        self._queue, self._callback, 
                        partial_left(_transfer_exception, error_queue)
                    )
                ) 
                for _ in range(self.num_runner)
            ],
            error_queue,
            threading.Thread(target=_handle_exception, args=(error_queue, self._exception_handler))
        )
        state.run()
        return state

    def put(self, x):
        if x is not Signal.IGNORE:
            self._queue.put(x, block=True, timeout=self.timeout)
    
    def release(self):
        self._queue.join()
        if self._state is not None:
            for _ in self._state.processes:
                self._queue.put(Signal.CANCEL)

            self._state.release()
        
        old_queue = self._queue
        old_queue.close()
        
        new_queue = mp.JoinableQueue(self._qsize)
        self._queue = new_queue
        del old_queue
        state = self._state
        del state
        
        super().release()

    def is_alive(self):        
        return (
            self.running 
            and self._state is not None 
            and any(p.is_alive() for p in self._state.processes)
        )


def _transfer_exception(error_queue:mp.JoinableQueue, data, e:Exception):
    error_queue.put((data, TraceableException(exception=e)))


def _handle_exception(error_queue:mp.JoinableQueue, exception_handler:Callable[[Any, Exception]]):
    signal = error_queue.get()
    if signal is Signal.CANCEL:
        return
    
    data, exception = signal
    exception:TraceableException
    
    original = exception.original 
    original.add_note(exception.info) #type:ignore
    exception_handler(data, original) #type:ignore
