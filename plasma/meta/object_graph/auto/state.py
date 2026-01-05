import inspect

from .context_graph import ContextGraph
from ...utils import get_caller_frame
from pathlib import Path
from .functional_context import FunctionalContext

CONTEXT_GRAPH = ContextGraph()
