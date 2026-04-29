import inspect

from .state import CONTEXT_GRAPH
from ...utils import get_caller_frame
from .functional_context import FunctionalContext


def init_context():
    caller = get_caller_frame()    
    package = inspect.getmodule(caller.frame).__package__ #type:ignore 
    
    return FunctionalContext(CONTEXT_GRAPH, package) # type:ignore


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
