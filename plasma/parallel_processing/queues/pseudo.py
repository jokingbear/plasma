from .base import Queue


class PseudoQueue(Queue):
    
    def __init__(self, name=None):
        super().__init__(name, 0)
    
    def _init_state(self):
        return None
    
    def put(self, x):
        assert self.running, 'queue need to be run first'        
        self._callback(x)
