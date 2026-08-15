import zarr
import numpy as np

from collections.abc import Sequence, Iterable
from typing import cast
from zarr.codecs import BloscCodec


class Tensor:
    
    def __init__(self, 
            filepath:str, 
            component_shapes:Sequence[Sequence[int]]
        ):
        self._root = zarr.open_array(filepath)
        self.shapes = component_shapes
    
    @property
    def chunk(self):
        return self._root.chunks[0]
    
    @property
    def shard(self) -> int:
        return self._root.shards[0] #type:ignore
    
    def get(self, args:int|list[int]|slice):
        array = cast(np.ndarray, self._root[args])
        flattend_shapes = _flattened_shapes(self.shapes)
        offset = 0
        for fshape, shape in zip(flattend_shapes, self.shapes):
            slice_args = slice(offset, offset + fshape)
            
            if len(array.shape) == 1:
                yield array[slice_args].reshape(*shape)
            else:
                yield array[:, slice_args].reshape(-1, *shape)
    
    def __getitem__(self, args:int|list[int]|slice):
        return self.get(args)
    
    def set(self, key:int|list[int]|slice, values:Iterable[np.ndarray]):
        values = [v for v in values]
        batch_size = values[0].shape[0] if len(values[0].shape) > 1 else 1
        
        values = np.concat([v.reshape(batch_size, -1) for v in values])
        if isinstance(key, int):
            key = [key]
        
        self._root[key] = values
    
    def __setitem__(self, key:int|list[int]|slice, values:Iterable[np.ndarray]):
        self.set(key, values)

    def reconfig(self, chunk:int, shard:int, compression:int):
        codec = BloscCodec(clevel=compression, shuffle='shuffle')
        shape = self._root.shape
        storage = self._root.store
        self._root.store_path.delete_sync()
        
        self._root = zarr.create_array(
            storage, shape=shape,
            chunks=(chunk, *shape[1:]),
            shards=(shard, *shape[1:]),
            dtype=np.float32,
            compressors=codec,
            overwrite=True,
        )
        return self
    
    @staticmethod
    def construct(
            filepath:str, 
            component_shapes:Sequence[Sequence[int]],
            num_data:int, chunk:int, shard:int,
            compression:int,
        ):
        dim_size = sum(_flattened_shapes(component_shapes))
        codec = BloscCodec(clevel=compression, shuffle='shuffle')
        zarr.create_array(
            filepath, 
            shape=[num_data, dim_size],
            chunks=[chunk, dim_size],
            shards=(shard, dim_size),
            compressors=codec
        )
        
        return Tensor(filepath, component_shapes)


def _flattened_shapes(shapes:Sequence[Sequence[int]]):
    for s in shapes:
        s = np.prod(s)
        yield cast(int, s)
