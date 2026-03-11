import networkx as nx
import typing

from .repr import Repr
from ...inquirer import is_data_model


class Representation(nx.DiGraph):
    
    def __init__(self, cls):
        super().__init__()
        
        root = ''
        self.__update(root, cls)

        self.root = root
    
    def __update(self, accessor, cls:type):
        origin, args = _analyze(cls)
        self.add_node(accessor, origin=origin, args=args)
        
        if issubclass(origin, (list, tuple)) and len(args) > 0 and is_data_model(args[0]):
            new_accessor = (*accessor, '@idx')
            self.add_edge(accessor, new_accessor)
            self.__update(new_accessor, args[0])
        elif is_data_model(origin):
            for a, at in origin.__annotations__.items():
                new_accessor = (*accessor, a)
                self.add_edge(accessor, new_accessor)
                self.__update(new_accessor, at)
        
    def origin(self, node) -> type:
        return self.nodes[node]['origin']
    
    def args(self, node) -> tuple[type]:
        return self.nodes[node]['args']
    
    def type(self, node):
        return self.origin(node), self.args(node)
    
    def __repr__(self):
        return Repr(self).run()


def _analyze(cls:type):
    origin = typing.get_origin(cls)
    
    if origin is None:
        return cls, ()
    else:
        return origin, typing.get_args(cls)
    