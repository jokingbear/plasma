import pickle
import lzma

from .protocols import Serializer


class Lzma(Serializer):
    
    def __init__(self, preset:int|None=None):
        super().__init__()
        self.preset = preset

    def serialize(self, x):
        contents = pickle.dumps(x)
        return lzma.compress(
            contents, preset=self.preset
        )

    def deserialize(self, x):
        contents = lzma.decompress(x)
        return pickle.loads(contents)
