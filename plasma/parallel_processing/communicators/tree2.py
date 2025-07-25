from .tree import TreeFlow
from ..queues import Queue
from ...functional import partials
from ._proxy import ProxyIO
from typing import Callable, Any


class StableTree(TreeFlow):
    
    def __init__(self):
        super().__init__()
        
        self._exception_handler = None
        self._initiated = False
    
    def on_exception(self, handler:Callable[[str, Any, Exception], None]):
        assert not self.running, \
            'tree is already running, please release it to register new exception handler'
        assert handler is not None, 'handler can not be None'

        self._exception_handler = handler
        
        return self

    def run(self):
        for n, q in self.queues.items():
            if n is not ProxyIO:
                assert q is not None, f'no queue registered for block {n}'
                exception_handler = self._exception_handler
                if exception_handler is not None and not self._initiated:
                    exception_handler = partials(exception_handler, n)
                    q.on_exception(exception_handler)

        if not self._initiated:
            self._initiated = True
            return super().run()
        else:
            for n, q in self.queues.items():
                q.run()
            return self
    
    @property
    def queues(self) -> dict[str, Queue]:
        return {n: attrs.get('queue', None) for n, attrs in self._module_graph.nodes.items()}

    def is_alive(self):
        return self.running and all(q.is_alive() for q in self.queues.values() if q is not None)
