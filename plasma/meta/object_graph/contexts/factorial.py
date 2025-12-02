from .base import Base
from ..factory import Factory
from ..links import Link
from ..types import Node


class FactorialContext(Base):

    def factory(self, name:str, overwrite=False):
        if (self.name, name) in self.graph and overwrite:
            self.remove_dependency(name)
        
        factory = Factory(name, self.name, self.graph)
        return factory

    def add_dependency(self, name, value, as_singleton=False):
        if isinstance(value, Factory):
            self.graph.merge(value.graph, overwrite=True)
            if self.name != value.context:
                self.graph.add_node(self.name, name, type=Node.FACTORY, value=None)
                self.graph.add_edge((self.name, name), (value.context, value.name), Link.DELEGATE_TO)
            else:
                value.name = name
                self.graph.update_node((self.name, value.name), (value.context, value.name))
            
            return self
        else:
            return super().add_dependency(name, value, as_singleton)
