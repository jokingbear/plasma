from .accessors import AccessorSchema


class StructSchema(dict):

    def __init__(self, accessors:AccessorSchema):
        super().__init__()

        for k in accessors:
            container = self
            components = k.split('.')
            for i, c in enumerate(components):
                if i == len(components) - 1:
                    current = container.setdefault(c, k)
                elif c == '@idx':
                    current = container[0]
                elif components[i + 1] == '@idx':
                    current = container.setdefault(c, [{}])
                else:
                    current = container.setdefault(c, {})
                
                container = current
