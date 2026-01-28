import networkx as nx

from typing import Callable, Iterable
from .segment import Segment
from ...functional import AutoPipe
from .position_path import PositionPath


class Solver(AutoPipe[[PositionPath], Iterable[Segment]]):
    
    def __init__(self, 
                position_graph:nx.DiGraph,
                db_path_arg_getter:Callable[[str], Iterable[int]],
            ):
        super().__init__()
        self.graph = position_graph
        self.db_path_arg_getter = db_path_arg_getter

    def run(self, position_path:PositionPath):
        scores = {n: self.graph.nodes[n]['score'] for n in position_path}
        shared_path_args = set(self.db_path_arg_getter(position_path.token(0)))
        start = offset = 0
        for offset in range(offset, len(position_path)):
            db_path_args = self.db_path_arg_getter(position_path.token(offset))
            updated_shared_paths = shared_path_args.intersection(db_path_args)
            if len(updated_shared_paths) == 0:
                yield Segment(position_path[start:offset], scores, shared_path_args)
                start = offset
                shared_path_args = set(db_path_args)

        yield Segment(position_path[start:offset + 1], scores, shared_path_args)
