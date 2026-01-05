import networkx as nx

from typing import Hashable
from .meta import Meta
from .inquirer import Inquirer
from .render import render


class ContextGraph(nx.DiGraph):
    
    def __init__(self):
        super().__init__()
        
        self._meta = Meta()
    
    def add_node(self, node_for_adding, **attr):
        super().add_node(node_for_adding, **attr)
        self._meta.add_name(*node_for_adding)

    def init_context(self, context):
        self._meta.init(context)
    
    @property
    def inquirer(self):
        return Inquirer(self._meta, self)

    def __repr__(self):
        return render(self._meta, self, self.inquirer)
