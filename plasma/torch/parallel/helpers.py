from torch.multiprocessing import set_start_method
from queue import Queue
from ...parallel_processing.queues import Signal, ExceptionHandler
from .pipe import InitPipe
from typing import Callable


def internal_run(queue:Queue, rank:int, processor:InitPipe[Callable], exception_handler:ExceptionHandler):
    is_not_cancelled = True
    exception_handler = exception_handler or ExceptionHandler()
    run_func = processor.run(rank)
    
    while is_not_cancelled:
        data = queue.get()

        is_not_cancelled = data is not Signal.CANCEL
        try:
            if is_not_cancelled:
                run_func(data)
        except Exception as e:
            exception_handler(data, e)
        finally:
            queue.task_done()
            del data


def init():
    set_start_method('spawn')
