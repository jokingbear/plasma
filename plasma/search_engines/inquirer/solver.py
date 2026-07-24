import networkx as nx

from typing import Callable, Iterable
from .segment import Segment
from .position_path import PositionPath
from ..index import Index


class Solver:
    
    def __init__(
            self, 
            index:Index,
            position_graph:nx.DiGraph,
            db_path_arg_getter:Callable[[str], Iterable[int]],
        ):
        super().__init__()
        self.index = index
        self.graph = position_graph
        self.db_path_arg_getter = db_path_arg_getter

    def __call__(self, position_path:PositionPath):        
        anchor = 0
        offset = 0
        prev_token = None
        shared_path_args = set()
        while offset < len(position_path):
            token = position_path.token(offset)
            db_path_args = [*self.db_path_arg_getter(token)]
            updated_shared_paths = shared_path_args.intersection(db_path_args)
            
            if prev_token is not None:
                edge_candidates = self.index.get_consecutive_candidates(prev_token, token)
                updated_shared_paths = updated_shared_paths.intersection(edge_candidates)

            if len(updated_shared_paths) == 0:
                if anchor < offset:
                    yield Segment(position_path[anchor:offset], shared_path_args)
                
                anchor = max(offset - 1, 0)
                anchor_paths = self.db_path_arg_getter(position_path.token(anchor))
                updated_shared_paths = set(db_path_args).intersection(anchor_paths)

            shared_path_args = updated_shared_paths
            offset += 1
            prev_token = token
        
        yield Segment(position_path[anchor:offset], shared_path_args)
