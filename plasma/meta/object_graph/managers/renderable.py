from .base import Manager


class RenderableManager(Manager):
    
    def __repr__(self):
        lines = []
        for c in self.contexts:
            context = self.init_context(c)
            lines.extend(repr(context).split('\n'))
        return '\n'.join(lines)
