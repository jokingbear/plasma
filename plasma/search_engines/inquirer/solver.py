import networkx as nx

from typing import Callable, Iterable
from .segment import Segment
from ...functional import AutoPipe
from .position_path import PositionPath


class Solver(AutoPipe[[PositionPath], Iterable[Segment]]):
    
    def __init__(
            self, 
            position_graph:nx.DiGraph,
            db_path_arg_getter:Callable[[str], Iterable[int]],
        ):
        super().__init__()
        self.graph = position_graph
        self.db_path_arg_getter = db_path_arg_getter

    def run(self, position_path:PositionPath):
        scores = dict[object, float]((n, self.graph.nodes[n]['score']) for n in position_path)
        
        anchor = 0
        offset = 0
        shared_path_args = set()
        while offset < len(position_path):
            db_path_args = [*self.db_path_arg_getter(position_path.token(offset))]
            updated_shared_paths = shared_path_args.intersection(db_path_args)
            if len(updated_shared_paths) == 0:
                if anchor < offset:
                    yield Segment(position_path[anchor:offset], scores, shared_path_args)
                
                anchor = max(offset - 1, 0)
                anchor_paths = self.db_path_arg_getter(position_path.token(anchor))
                updated_shared_paths = set(db_path_args).intersection(anchor_paths)

            shared_path_args = updated_shared_paths
            offset += 1
        
        yield Segment(position_path[anchor:offset], scores, shared_path_args)
