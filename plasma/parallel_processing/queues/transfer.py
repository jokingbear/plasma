from .base import Queue
from multiprocessing import JoinableQueue
from ...functional import partials, decorators
from .utils import internal_run
from threading import Thread
from .signals import Signal


class TransferQueue(Queue[Thread]):

    def __init__(self, name=None, qsize=0):
        super().__init__(name)

        self._receiver = JoinableQueue(qsize)

    @decorators.propagate(Signal.IGNORE)
    def put(self, x):
        self._receiver.put(x, block=True)

    def _init_state(self):
        runner = partials(internal_run, self._receiver, self._callback, self._exception_handler)
        thread = Thread(target=runner) 
        thread.start()
        return thread

    def release(self):
        self._receiver.put(Signal.CANCEL)
        self._state.join()

        super().release()

    def is_alive(self):
        return self.running and self._state.is_alive()
