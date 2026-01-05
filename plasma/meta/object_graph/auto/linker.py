from types import ModuleType
from ...utils import get_caller_frame
from pathlib import Path
from .state import CONTEXT_GRAPH
from warnings import warn
from .context_graph import Node
from .context import Context


def link_name(context:Context, *excludes:str):
    caller = get_caller_frame()
    current_context = CONTEXT_GRAPH.inquirer.find_context(Path(caller.filename))
    linking_context = context.name
    
    current_names = {node_name for node_name 
                     in CONTEXT_GRAPH.inquirer.node_names(current_context)}
    
    candidate_names = {node_name for node_name 
                       in CONTEXT_GRAPH.inquirer.node_names(linking_context)}
    
    shared_names = current_names.intersection(candidate_names).difference(excludes)
    if len(shared_names) == 0:
        warn(f'{current_context} does not share any name with {linking_context}')
    else:
        for n in shared_names:
            ntype = CONTEXT_GRAPH.inquirer.type((current_context, n))
            
            if ntype is not Node.LEAF:
                warn(
                    f'overriding non leaf object {n} in {current_context} '
                    f'with {n} in {linking_context}'
                )
            
                CONTEXT_GRAPH.remove_node((current_context, n))
            
            CONTEXT_GRAPH.add_node((current_context, n), type=Node.DELEGATE)
            CONTEXT_GRAPH.add_edge((current_context, n), (linking_context, n))
