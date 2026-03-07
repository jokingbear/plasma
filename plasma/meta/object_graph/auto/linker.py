from warnings import warn
from .context_graph import Node, ContextGraph
from .context import Context
from ....functional import AutoPipe
from .delegator import Delegator


class Linker(AutoPipe):
    
    def __init__(self, graph:ContextGraph):
        super().__init__()
        self.graph = graph
    
    def run(self, context1:Context, context2:Context, source:str, *excludes:str):
        current_context = context1.name
        linking_context = context2.name
        
        inquirer = self.graph.inquirer
        current_names = {*inquirer.node_names(current_context)}
        candidate_names = {*inquirer.node_names(linking_context)}
        
        shared_names = current_names.intersection(candidate_names).difference(excludes)
        return self.run_map(context1, context2, source, {n:n for n in shared_names})

    def run_map(self, context1:Context, context2:Context, source:str, map:dict):
        current_context = context1.name
        linking_context = context2.name
        
        if len(map) == 0:
            warn('empty map')
        
        delegator = Delegator(self.graph, current_context, source)
        for source, target in map.items():
            delegator.run(source, linking_context, target)
