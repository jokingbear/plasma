from .repr import Repr

from ..accessor import build


class Schema(Repr):
    
    def __init__(self, root:type):
        super().__init__()
        self.root = build('', root)
