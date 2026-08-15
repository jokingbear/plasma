import zstd

from .pickle import Pickler


class Zstd(Pickler):
    
    def __init__(self, level:int=3):
        super().__init__()
        self.level = level

    def serialize(self, x):
        contents = super().serialize(x)
        return zstd.compress(
            contents, self.level
        )

    def deserialize(self, x):
        contents = zstd.decompress(x)
        return super().deserialize(contents)
