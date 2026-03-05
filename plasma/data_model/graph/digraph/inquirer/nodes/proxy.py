from .base import Nodes
from .projector import Projector
from typing import Iterable, Hashable


class Proxy[T](Nodes[T]):
    
    def __init__(self, index, inquirer:T, ids:Iterable[Hashable]):
        super().__init__(index, ids, Projector(inquirer, [], [], None))
