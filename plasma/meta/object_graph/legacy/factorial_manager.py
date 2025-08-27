from .dependency_manager import DependencyManager


class FactoryManager(DependencyManager):
    
    def init_factory(self, name:str):
        factory = DependencyFactory(name, self)
        
        if name in self._dep_graph:
            self._dep_graph.remove_node(name)
        
        self._dep_graph.add_node(name, factory=factory)
        return factory
    
    def _link_factory(self, factory_name:str, *names:str):
        for n in names:
            self._dep_graph.add_edge(factory_name, n)
        
        return self


class DependencyFactory:
    
    def __init__(self, factory_name:str, manager:FactoryManager):
        self.name = factory_name
        self._dep_manager = manager
        self._registered_names = []
    
    def register(self, *names):  
        assert len(names) > 0, 'must at least have one name'
        self._registered_names.extend(names)
              
        def decorate(cls):
            for n in names:
                self._dep_manager.add_dependency(n, cls)
            
            self._dep_manager._link_factory(self.name, *names)
            return cls
        
        return decorate
    
    def register_singleton(self, name, obj):
        self._registered_names.append(name)
        self._dep_manager.add_dependency(name, obj, as_singleton=True)
        self._dep_manager._link_factory(self.name, name)
        return self
    
    def __setitem__(self, key, obj):
        self.register_singleton(key, obj)
            
    def __repr__(self):
        return (
            f'{type(self).__name__}(\n'
            f'\tname={self.name},\n'
            f'\tegistered_names={self._registered_names}\n'
            ')'
        )
