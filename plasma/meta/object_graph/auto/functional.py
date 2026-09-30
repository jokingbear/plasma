import inspect

from .state import CONTEXT_GRAPH
from ...utils import get_caller_frame
from .functional_context import FunctionalContext


def init_context(inherit:bool=False):
    caller = get_caller_frame()    
    package:str = inspect.getmodule(caller.frame).__package__ #type:ignore 
    
    if inherit:
        hierachy_names = package.split('.')
        for i, _ in enumerate(hierachy_names[::-1]):
            if i == 0:
                continue
            
            parent = '.'.join(hierachy_names[:-i])
            if parent not in CONTEXT_GRAPH:
                continue
            package = parent
            break
        
    return FunctionalContext(CONTEXT_GRAPH, package)


def register(**blocks:type|object):
    caller = get_caller_frame()
    file = caller.filename
    package = inspect.getmodule(caller.frame).__package__ #type:ignore 
    
    context = CONTEXT_GRAPH.inquirer.find_context(package) #type:ignore 
    if context is None:
        raise ImportError(
                    f'{file} does not belong to any context, '
                    'use init_context first'
                )
    
    return FunctionalContext(CONTEXT_GRAPH, context).register(source=file, **blocks)


def inspect_graph():
    print(repr(CONTEXT_GRAPH))
