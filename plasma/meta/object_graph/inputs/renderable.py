import re

from .functional import InitiableInputs as Inputs


class RenderableInputs(Inputs):
    
    def to_dict(self):
        results = {}
        for k in self.__annotations__:
            if hasattr(self, k):
                value = getattr(self, k)
                if isinstance(value, Inputs):
                    value = value.to_dict()
                
                results[k] = value

        return results
    
    def __repr__(self):
        return rendered(self.to_dict())


def rendered(d:dict):
    lines = ['{']
    indent = ' ' * 4
    for k, v in d.items():
        if isinstance(v, str):
            v = f'"{v}"'
        
        if isinstance(v, dict):
            rendered_dict = rendered(v)
            dict_lines = rendered_dict.split('\n')
            dict_lines[0] = f'{k}: {{'
            dict_lines[-1] += ','
            lines.extend(f'{indent}{l}' for l in dict_lines)
        else:
            lines.append(f'{indent}{k}: {v},')

    lines.append('}')
    return '\n'.join(lines)
