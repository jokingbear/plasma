from .context_graph import ContextGraph
from ...utils import get_caller_frame
from pathlib import Path
from types import ModuleType
from .functional_context import FunctionalContext

CONTEXT_GRAPH = ContextGraph()


def init_context():
    caller = get_caller_frame()
    caller_file = Path(caller.filename)

    CONTEXT_GRAPH.init_context(caller_file.parent)
    return FunctionalContext(CONTEXT_GRAPH, caller_file.parent)
