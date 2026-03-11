class AccessorState(dict[str, object]):
    
    def __init__(self, accessor_schema, obj):
        super().__init__()

        for a in accessor_schema:
            self.__update(obj, None, a.split('.'))

    def __update(self, obj, key, path):
        if len(path) == 0:
            self[key] = obj
        elif path[0] == '@idx':
            assert isinstance(obj, (tuple, list)), f'expect list or tuple at {key}'
            for i, v in enumerate(obj):
                self.__update(v, f'{key}.{i}', path[1:])
        else:
            next_key = f'{key}.{path[0]}' if key is not None else path[0]
            if obj is None:
                value = None
                path = []
            else:
                assert hasattr(obj, path[0]), f'no attribute {path[0]} for {obj}'
                value = getattr(obj, path[0])

            self.__update(value, next_key, path[1:])
