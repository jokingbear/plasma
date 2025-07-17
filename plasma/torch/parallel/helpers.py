from torch.multiprocessing import set_start_method
from queue import Queue
from ...parallel_processing.queues import Signal, ExceptionHandler
from .pipe import TorchPipe


def internal_run(queue:Queue, rank:int, processor:TorchPipe, exception_handler:ExceptionHandler):
    is_not_cancelled = True
    exception_handler = exception_handler or ExceptionHandler()
    processor.process_init(rank)
    
    while is_not_cancelled:
        data = queue.get()

        is_not_cancelled = data is not Signal.CANCEL
        try:
            if is_not_cancelled:
                processor(data)
        except Exception as e:
            exception_handler(data, e)

        queue.task_done()


def init():
    set_start_method('spawn')
