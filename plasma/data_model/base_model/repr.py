def render_lines(field_name:str, obj, lines:list, indent:str):
    if field_name is None:
        prefix = ''
    else:
        prefix = f'|-{field_name}='

    if hasattr(type(obj), '__data_model'):
        lines.append(f'{indent}{prefix}{type(obj).__name__}')
        for a in obj.__annotations__:
            render_lines(a, getattr(obj, a), lines, indent + '  ')
    else:
        if isinstance(obj, (tuple, list)):
            lines.append(f'{indent}{prefix}')
            element_reprs = []
            multi_line = False
            for o in obj:
                olines = repr(o).split('\n')
                multi_line = len(olines) > 1
                element_reprs.extend(olines)
            
            if multi_line:
                lines[-1] = lines[-1][:-1] + ':'
                lines.extend(indent + ' ' *len(prefix) + e for e in element_reprs)
                lines.append(f'{indent}')
            else:
                lines[-1] += '[' + ', '.join(element_reprs) + ']'
        else:
            obj_repr = repr(obj)
            obj_lines = obj_repr.split('\n')
            obj_lines[0] = prefix + obj_lines[0]
            lines.extend(indent + l for l in obj_lines)
