from .base import Base


class RenderableManager(Base):
    
    def __repr__(self):
        lines = []
        for c in self.contexts:
            context = self.init_context(c)
            lines.extend(repr(context).split('\n'))
        return '\n'.join(lines)
