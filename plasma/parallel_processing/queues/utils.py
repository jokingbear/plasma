from queue import Queue
from typing import Callable, Any
from .signals import Signal


def internal_run(
        queue:Queue, 
        processor:Callable[[Any], None], 
        exception_handler:Callable[[Any, Exception], None]
    ):
    while True:
        data = queue.get()
        try:
            if data is Signal.CANCEL:
                break

            processor(data)
        except Exception as e:
            if exception_handler is None:
                raise e
            exception_handler(data, e)
        finally:
            queue.task_done()
