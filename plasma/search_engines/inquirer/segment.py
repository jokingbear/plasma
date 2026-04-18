from typing import NamedTuple, Iterable
from .position_path import PositionPath


class Segment(NamedTuple):
    position_path:PositionPath
    db_path_args:Iterable[int]
    
    @property
    def qtoken_start(self):
        return self.position_path.offset(0)
    
    @property
    def qtoken_end(self):
        return self.position_path.offset(-1) + 1


class Match(NamedTuple):
    qchar_start:int
    qchar_end:int
    
    db_arg:int
    db_char_start:int
    db_char_end:int
    db_value:str
    
    matching_score:float
    coverage_score:float
    matched_len:int
    harmonic_score:float
    
    def update(self, offset:int):
        qstart, qend, *remaining = self
        return Match(
            qstart + offset,
            qend + offset,
            *remaining # type: ignore
        )
