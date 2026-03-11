from .representation import GraphRepresetation
from .realization import Realization


class Schema:
    
    def __init__(self, cls:type):
        self.rep = GraphRepresetation(cls)

    def realize(self, obj):
        return Realization(self.rep, obj)
    
    def __repr__(self):
        return repr(self.representation)
