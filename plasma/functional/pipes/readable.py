class ReadableClass:
    
    def __init__(self):
        self._marked_attributes = []

    def __setattr__(self, key:str, value):
        if key[0] != '_' and key not in self._marked_attributes:
            self._marked_attributes.append(key)

        super().__setattr__(key, value)

    def __repr__(self):
        lines = [f'{type(self).__name__}(']
        indent = ' ' * 2
        for attr in self._marked_attributes:
            val = getattr(self, attr)
            val_rep = repr(val)
            val_lines = val_rep.split('\n')
            val_lines[0] = f'{attr}={val_lines[0]}'
            val_lines[-1] += ','
            lines.extend(indent + vl for vl in val_lines)
        lines.append(')')
        return '\n'.join(lines)
