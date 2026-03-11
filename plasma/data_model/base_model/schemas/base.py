from .representation import Representation
from .realization import Realization


class Schema:
    
    def __init__(self, cls:type):
        self.rep = Representation(cls)

    def realize(self, obj):
        return Realization(self.rep, obj)
    
    def __repr__(self):
        return repr(self.rep)
