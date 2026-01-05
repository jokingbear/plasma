import inspect

from .context_graph import ContextGraph
from ...utils import get_caller_frame
from pathlib import Path
from .functional_context import FunctionalContext

CONTEXT_GRAPH = ContextGraph()


def init_context():
    caller = get_caller_frame()    
    package = inspect.getmodule(caller.frame).__package__
    
    return FunctionalContext(CONTEXT_GRAPH, package)


def register(**blocks:type|object):
    caller = get_caller_frame()
    file = caller.filename
    package = inspect.getmodule(caller.frame).__package__
    
    context = CONTEXT_GRAPH.inquirer.find_context(package)
    if context is None:
        raise ImportError(
                    f'{file} does not belong to any context, '
                    'use init_context first'
                )
    
    return FunctionalContext(CONTEXT_GRAPH, context).register(source=file, **blocks)
