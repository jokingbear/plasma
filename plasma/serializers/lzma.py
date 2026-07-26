import lzma

from .pickle import Pickler


class Lzma(Pickler):
    
    def __init__(self, preset:int|None=None):
        super().__init__()
        self.preset = preset

    def serialize(self, x):
        contents = super().serialize(x)
        return lzma.compress(
            contents, preset=self.preset
        )

    def deserialize(self, x):
        contents = lzma.decompress(x)
        return super().deserialize(contents)

