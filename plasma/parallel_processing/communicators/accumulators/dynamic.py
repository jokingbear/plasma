from .base import Accumulator


class DynamicAccumulator[D, A](Accumulator[D, A]):
    
    def __init__(self, process_base=False, ignore_none=True, count_none=True):
        super().__init__(0, 1e-2, process_base, ignore_none, count_none)
        self.init_state()
    
    def wait(self, total:int, **tqdm_kwargs):
        self.total = total
        return super().wait(**tqdm_kwargs)

    def init_state(self):...
