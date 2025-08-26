from .base import Base
from ..types import Node
from ..links import Link
from warnings import warn


class FactorialContext(Base):

    def init_factory(self, name:str, overwrite=False):
        if name in self and overwrite:
            self.remove_dependency(name)
            
        factory = DependencyFactory(name, self)
        self._add_node(name, type=Node.FACTORY, value=factory)
        return factory
    
    def _link_components(self, factory_name, *names):
        for n in names:
            self._add_edge(factory_name, n, Link.CONTAINS)


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
            
    def __repr__(self):
        return (
            f'{type(self).__name__}(\n'
            f'\tname={self.name},\n'
            ')'
        )
