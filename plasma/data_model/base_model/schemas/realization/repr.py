import networkx as nx

from rich.tree import Tree
from .....utils import rich_repr


class Repr:
    
    def __init__(self, realization:nx.DiGraph):
        self.graph = realization
    
    def __call__(self, root):
        tree = Tree(self._render_node(root))
        self._iterate(tree, root)

        return rich_repr(tree)
    
    def _iterate(self, tree:Tree, node):
        for s in self.graph.successors(node):
            srepr = self._render_node(s)
            new_tree = tree.add(srepr)
            self._iterate(new_tree, s)

    def _render_node(self, node):
        if self.graph.in_degree(node) == 0:
          return type(self.graph.nodes[node]['value']).__name__
      
        elif self.graph.out_degree(node) == 0:
            return f'{node[-1]}={self.graph.nodes[node]['value']}'
        
        else:
            return f'{node[-1]}:{type(self.graph.nodes[node]['value']).__name__}'
