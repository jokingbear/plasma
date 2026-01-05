from .context_graph import ContextGraph
from ...utils import get_caller_frame
from pathlib import Path
from .functional_context import FunctionalContext

CONTEXT_GRAPH = ContextGraph()


def init_context():
    caller = get_caller_frame()
    caller_file = Path(caller.filename)

    CONTEXT_GRAPH.init_context(caller_file.parent)
    return FunctionalContext(CONTEXT_GRAPH, caller_file.parent)


def register(**blocks:type|object):
    caller = get_caller_frame()
    file = Path(caller.filename)
    context = CONTEXT_GRAPH.inquirer.find_context(file)
    if context is None:
        raise ImportError(
                    f'{file} does not belong to any context, '
                    'use init_context first'
                )
    
    return FunctionalContext(CONTEXT_GRAPH, context).register(source=file, **blocks)
