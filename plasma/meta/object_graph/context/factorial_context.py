from .context import Context
from ..types import Node
from ..links import Link


class FactorialContext(Context):

    def init_factory(self, name:str):
        factory = DependencyFactory(name, self.graph)
        
        if name in self.graph:
            self.graph.remove_node(name)
        
        self.graph.add_node(name, type=Node.FACTORY, value=factory)
        return factory
    
    def _link_factory(self, factory_name, *names):
        factory_node_id = self.node_id(factory_name)
        
        for n in names:
            node_id = self.node_id(n)
            self.graph.add_edge(factory_node_id, node_id, Link.CONTAINS)


class DependencyFactory:
    
    def __init__(self, factory_name:str, context:FactorialContext):
        self.name = factory_name
        self.context = context
        self._registered_names = []
    
    def register(self, *names):  
        assert len(names) > 0, 'must at least have one name'
        self._registered_names.extend(names)
              
        def decorate(cls):
            for n in names:
                self.context.add_dependency(n, cls)
            
            self.context._link_factory(self.name, *names)
            return cls
        
        return decorate
    
    def register_singleton(self, name, obj):
        self._registered_names.append(name)
        self.context.add_dependency(name, obj, as_singleton=True)
        self.context._link_factory(self.name, name)
        return self
    
    def __setitem__(self, key, obj):
        self.register_singleton(key, obj)
            
    def __repr__(self):
        return (
            f'{type(self).__name__}(\n'
            f'\tname={self.name},\n'
            f'\tregistered_names={self._registered_names}\n'
            ')'
        )
