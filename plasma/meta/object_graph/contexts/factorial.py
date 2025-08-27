from .base import Base
from ..types import Node
from ..links import Link


class FactorialContext(Base):

    def factory(self, name:str, overwrite=False):
        if (self.name, name) in self.graph and overwrite:
            self.remove_dependency(name)
        
        factory_id = self.name, name
        factory = DependencyFactory(name, self)
        self.graph.add_node(*factory_id, type=Node.FACTORY, value=factory)
        return factory
    
    def _link_components(self, factory_name, *names):
        factory_id = self.name, factory_name
        for n in names:
            node_id = self.name, n
            self.graph.add_edge(factory_id, node_id, Link.SUBITEM)


class DependencyFactory:
    
    def __init__(self, factory_name:str, context:FactorialContext):
        self.name = factory_name
        self.context = context
    
    def register(self, *names):  
        assert len(names) > 0, 'must at least have one name'
              
        def decorate(cls):
            for n in names:
                self.context.add_dependency(n, cls)
            
            self.context._link_components(self.name, *names)
            return cls
        
        return decorate
    
    def register_singleton(self, name, obj):
        self.context.add_dependency(name, obj, as_singleton=True)
        self.context._link_components(self.name, name)
        return self
    
    def __setitem__(self, key, obj):
        self.register_singleton(key, obj)
