from ..schemas import Realization


class AccessorState(dict[str, object]):
    
    def __init__(self, real:Realization):
        super().__init__()

        for p in real.endpoints:
            value = real.value(p)
            self['.'.join(p[1:])] = value
