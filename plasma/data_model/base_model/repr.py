from .meta import Readable


def render_lines(field_name:str, obj, lines:list, indent:str):
    if field_name is None:
        prefix = ''
    else:
        prefix = f'|-{field_name}='

    if isinstance(type(obj), Readable):
        lines.append(f'{indent}{prefix}{type(obj).__name__}')
        for a in obj.__annotations__:
            render_lines(a, getattr(obj, a), lines, indent + '  ')
    else:
        obj_repr = repr(obj)
        obj_lines = obj_repr.split('\n')
        obj_lines[0] = prefix + obj_lines[0]
        lines.extend(indent + l for l in obj_lines)
