from .context_graph import ContextGraph, Node
from warnings import warn


class Delegator:
    
    def __init__(self, graph:ContextGraph, context:str, source:str):
        self.graph = graph
        self.context = context
        self.source = source
    
    def run(self, name, other_context, other_name):
        other_id = other_context, other_name 
        node_id = self.context, name
        
        assert other_id in self.graph
        inquirer = self.graph.inquirer
        
        if node_id in self.graph and inquirer.type(node_id) is not Node.LEAF:
            file, = inquirer.select(node_id, 'source')
            warn(f'{name} is already registered in {self.context} in {file}, overriding with {self.source}')
            self.graph.remove_node(node_id)
        
        self.graph.add_node(node_id, type=Node.DELEGATE, source=self.source)
        self.graph.add_edge(node_id, other_id)
