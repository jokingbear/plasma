import networkx as nx

from .base import Inquirer
from .nodes import Nodes as _Nodes


class NodeIterator[T:nx.DiGraph](_Nodes[Inquirer[T]]):...
