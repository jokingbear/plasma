import networkx as nx

from rich.tree import Tree
from rich.console import Console
from typing import Any, Callable, Sequence


class Repr:
    
    def __init__(
            self, 
            root, graph:nx.DiGraph, 
            type_getter:Callable[[Any], tuple[type, Sequence[type]]]
        ):
        self.root = root
        self.graph = graph
        self.type_getter = type_getter

    def __call__(self):
        tree = Tree('')
        self._iterate(self.root, tree)

        with Console(force_terminal=True, force_jupyter=False) as console:
            with console.capture() as capture:
                console.print(tree.children[0])    
            return capture.get()[1:]

    def _iterate(self, node, tree:Tree): #type:ignore
        origin, args = self.type_getter(node)
        
        type_str = origin.__name__
        if len(args) > 0:
            type_str += f'[{','.join(a.__name__ for a in args)}]'
        key = '' if len(node) == 0 else node[-1]
        tree = tree.add(f'{key}:{type_str}')

        for s in self.graph.successors(node):
            self._iterate(s, tree)
