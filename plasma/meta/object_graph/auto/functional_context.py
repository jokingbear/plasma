from .context import Context
from .linker import link_name
from .registrator import Registrator
from ...utils import get_caller_frame


class FunctionalContext(Context):
    
    def link_name(self, context:Context, *excludes:str):
        link_name(self, context, *excludes)
        return self
    
    def register(self, **blocks):
        caller = get_caller_frame()
        for node_name, block in blocks.items():
            registrator = Registrator(self.graph, self.name, node_name, caller.filename)
            if isinstance(block, type):
                registrator.register_type(block)
            else:
                registrator.register_singleton(block)

        return self
