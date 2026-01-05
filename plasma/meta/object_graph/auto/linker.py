from warnings import warn
from .context_graph import Node, ContextGraph
from .context import Context
from ....functional import AutoPipe


class Linker(AutoPipe):
    
    def __init__(self, graph:ContextGraph):
        super().__init__()
        self.graph = graph
    
    def run(self, context1:Context, context2:Context, *excludes:str):
        current_context = context1.name
        linking_context = context2.name
        
        inquirer = self.graph.inquirer
        current_names = {*inquirer.node_names(current_context)}
        candidate_names = {*inquirer.node_names(linking_context)}
        
        shared_names = current_names.intersection(candidate_names).difference(excludes)
        if len(shared_names) == 0:
            warn(f'{current_context} does not share any name with {linking_context}')
        else:
            for n in shared_names:
                ntype = inquirer.type((current_context, n))
                
                if ntype is not Node.LEAF:
                    warn(
                        f'overriding non leaf object {n} in {current_context} '
                        f'with {n} in {linking_context}'
                    )
                
                    self.graph.remove_node((current_context, n))
                
                self.graph.add_node((current_context, n), type=Node.DELEGATE)
                self.graph.add_edge((current_context, n), (linking_context, n))
