from .context_graph import ContextGraph
from ...utils import get_caller_frame
from pathlib import Path
from typing import Callable
from .factory import Factory
from .registrator import Registrator

CONTEXT_GRAPH = ContextGraph()


def init_context():
    caller = get_caller_frame()
    caller_file = Path(caller.filename)

    CONTEXT_GRAPH.init_context(caller_file.parent)


def register(name:str):
    caller = get_caller_frame()
    registrator = Registrator(CONTEXT_GRAPH, caller, name)
    
    def decorator(cls:type|Callable):
        registrator.register_type(cls)
        return cls

    return decorator


def register_singleton(name:str, singleton:object):
    caller = get_caller_frame()
    registrator = Registrator(CONTEXT_GRAPH, caller, name)
    registrator.register_singleton(singleton)
