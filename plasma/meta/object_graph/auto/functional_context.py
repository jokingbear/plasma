from .context import Context
from .linker import Linker
from .registrator import Registrator
from ...utils import get_caller_frame
from .factory import Factory


class FunctionalContext(Context):
    
    def __init__(self, graph, context):
        super().__init__(graph, context)
        
        self.linker = Linker(self.graph)
    
    def link_name(self, context:Context, *excludes:str):
        self.linker.run(self, context, *excludes)
        return self
    
    def register(self, source:str=None, **blocks):
        if source is None:
            caller = get_caller_frame()
            source = caller.filename

        for node_name, block in blocks.items():
            registrator = Registrator(self.graph, self.name, node_name, source)
            if isinstance(block, type):
                registrator.register_type(block)
            else:
                registrator.register_singleton(block)

        return self

    def factory(self, name:str):
        caller = get_caller_frame()
        return Factory(name, self.graph, self.name, caller.filename)
