import torch.multiprocessing as tmp

from ...parallel_processing.queues import Queue, Signal
from ...functional.decorators import propagate
from .pipe import TorchPipe
from .helpers import internal_run


class CudaQueue(Queue[list[tmp.Process]]):
    
    def __init__(self, name=None, num_runner=1, timeout=0, qsize=0):
        super().__init__(name, num_runner)
        
        self._queue = tmp.JoinableQueue(maxsize=qsize)
        self.timeout = timeout
    
    def _init_state(self):
        processes = [tmp.Process(target=internal_run, args=(self._queue, i, self._callback, self._exception_handler)) 
                     for i in range(self.num_runner)]
        [p.start() for p in processes]
        return processes
    
    def register_callback(self, callback):
        assert isinstance(callback, TorchPipe), \
            f'TorchQueue only receive TorchPipe as callback, currently: {type(callback)}'
        return super().register_callback(callback)

    def chain(self, callback):
        self._callback = self._callback.chain(callback)
        return self

    @propagate(Signal.IGNORE)
    def put(self, x):
        return self._queue.put(x, block=True, timeout=self.timeout)

    def release(self):
        self._queue.join()
        if self._state is not None:
            for _ in self._state:
                self.put(Signal.CANCEL)
            self._queue.join()

            for p in self._state:
                p.join()
                p.terminate()
        
        super().release()

    def is_alive(self):        
        return self.running and any(p.is_alive() for p in self._state)
