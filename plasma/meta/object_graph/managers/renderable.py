from .base import Base
from ..contexts import Context


class RenderableManager(Base):
    
    def __repr__(self):
        lines = []
        for c in self.contexts:
            context = Context(self.graph, c)
            lines.extend(repr(context).split('\n'))
        return '\n'.join(lines)
