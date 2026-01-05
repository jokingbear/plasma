from .context_graph import ContextGraph
from ...utils import get_caller_frame
from pathlib import Path
from .registrator import Registrator
from .context import Context
from types import ModuleType

CONTEXT_GRAPH = ContextGraph()


def init_context():
    caller = get_caller_frame()
    caller_file = Path(caller.filename)

    CONTEXT_GRAPH.init_context(caller_file.parent)


def register(**blocks:type|object):
    caller = get_caller_frame()
    for name, block in blocks.items():
        registrator = Registrator(CONTEXT_GRAPH, caller, name)
        if isinstance(block, type):
            registrator.register_type(block)
        else:
            registrator.register_singleton(block)


def get_context(module:ModuleType):
    return Context(CONTEXT_GRAPH, module)
