class Readable(type):
    
    def __repr__(cls):
        lines = [super().__repr__()]
        for name, annotation in cls.__annotations__.items():
            if type(annotation) is Readable:
                sub_lines = repr(annotation).split('\n')
                sub_lines[0] = f'{name}:{sub_lines[0]}'
                lines.extend('\t' + l for l in sub_lines)
            else:
                lines.append(f'\t{name}:{annotation}')
        return '\n'.join(lines)
