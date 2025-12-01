from .base import Base
from ..factory import Factory


class FactorialContext(Base):

    def factory(self, name:str, overwrite=False):
        if (self.name, name) in self.graph and overwrite:
            self.remove_dependency(name)
        
        factory = Factory(name, self.name, self.graph)
        return factory
