from .context import Context
from .linker import Linker
from .registrator import Registrator
from ...utils import get_caller_frame
from .factory import Factory
from .delegator import Delegator
from pathlib import Path


class FunctionalContext(Context):
    
    def __init__(self, graph, context):
        super().__init__(graph, context)
        
        self.linker = Linker(self.graph)
    
    def link_name(self, context:Context, *excludes:str):
        caller = get_caller_frame()
        source = caller.filename
        self.linker.run(self, context, source, *excludes)
        return self
    
    def register(self, source:str=None, **blocks):
        if source is None:
            caller = get_caller_frame()
            source = caller.filename

        for node_name, block in blocks.items():
            if isinstance(block, Factory) and block.context_name != self.name:
                delegator = Delegator(self.graph, self.name, source)
                delegator.run(node_name, block.context_name, block.name)

            registrator = Registrator(self.graph, self.name, node_name, source)
            if isinstance(block, type):
                registrator.register_type(block)
            else:
                registrator.register_singleton(block)

        return self

    def factory(self, name:str=None):
        caller = get_caller_frame()
        name = name or Path(caller.filename).parent.name
        return FunctionalFactory(name, self.graph, self.name, caller.filename)


class FunctionalFactory(Factory):
    
    @property
    def context(self):
        return FunctionalContext(self.graph, self.context_name)
