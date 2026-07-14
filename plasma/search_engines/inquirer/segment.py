from dataclasses import dataclass
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

@dataclass
class Match:
    query:"QueryMatch"
    db:"DBMatch"
    score:"Score"
    
    def update(self, offset:int):
        return Match(
            QueryMatch(
                offset + self.query.start,
                offset + self.query.end
            ),
            self.db, self.score,
        )


@dataclass
class QueryMatch:
    start:int
    end:int
    
    def slice(self, query:str):
        return query[self.start:self.end]


@dataclass
class DBMatch:
    arg:int
    start:int
    end:int
    value:str
    
    def slice(self):
        return self.value[self.start:self.end]


@dataclass
class Score:
    substring:float
    coverage:float
    token_len:int
    harmonic:float
