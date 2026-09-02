import zarr
import numpy as np
import os
import shutil

from collections.abc import Sequence, Iterable
from typing import cast, Any, Literal
from zarr.codecs import BloscCodec
from zarr.experimental.cache_store import CacheStore
from zarr.storage import MemoryStore, LocalStore


class TensorStorage:
    
    def __init__(self, 
            filepath:str, *, 
            cache_size_mb:int=0,
            cache_expiration_seconds:int|Literal['infinity']=24 * 3600,
        ):
        if cache_size_mb > 0:
            memory = MemoryStore()
            physical = LocalStore(filepath)
            store = CacheStore(
                physical, 
                cache_store=memory, 
                max_age_seconds=cache_expiration_seconds,
                max_size=cache_size_mb * 1024 * 1024
            )
        else:
            store = filepath

        array = zarr.open_array(store)
        self._root = array
    
    @property
    def chunk(self):
        return self._root.chunks[0]
    
    @property
    def shard(self) -> int:
        return self._root.shards[0] #type:ignore
    
    @property
    def shapes(self) -> Sequence[Sequence[int]]:
        return self._root.attrs['component_shapes'] #type:ignore
    
    def get(self, args:int|list[int]|slice|np.ndarray):
        array = cast(np.ndarray, self._root[args])
        flattend_shapes = _flattened_shapes(self.shapes)
        offset = 0
        for fshape, shape in zip(flattend_shapes, self.shapes):
            slice_args = slice(offset, offset + fshape)
            if len(array.shape) == 1:
                yield array[slice_args].reshape(*shape)
            else:
                yield array[:, slice_args].reshape(-1, *shape)
                    
    def __getitem__(self, args:int|list[int]|slice|np.ndarray):
        return self.get(args)
    
    def set(self, key:int|list[int]|slice|np.ndarray, values:Iterable[np.ndarray]):
        values = [v for v in values]
        batch_size = values[0].shape[0] if len(values[0].shape) > 1 else 1
        
        values = np.concat([v.reshape(batch_size, -1) for v in values], axis=-1)
        if isinstance(key, int):
            key = [key]
        
        self._root[key] = values
    
    def __setitem__(self, key:int|list[int]|slice|np.ndarray, values:Iterable[np.ndarray]):
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
    
    def __repr__(self):
        return f'{type(self).__name__}(shapes={self._root.shape[0], *self.shapes})'
    
    @staticmethod
    def construct(
            filepath:str, dtype:Any,
            component_shapes:Sequence[int|Sequence[int]],
            num_data:int, chunk:int, shard:int,
            compression:int,
        ):
        if os.path.exists(filepath):
            shutil.rmtree(filepath)

        standardized_shapes = [[s] if isinstance(s, int) else s for s in component_shapes]
        dim_size = sum(_flattened_shapes(standardized_shapes))
        codec = BloscCodec(clevel=compression, shuffle='shuffle')
        zarr.create_array(
            filepath, dtype=dtype,
            shape=[num_data, dim_size],
            chunks=[chunk, dim_size],
            shards=(shard, dim_size),
            compressors=codec,
            attributes={'component_shapes': standardized_shapes},
        )
        
        return TensorStorage(filepath)


def _flattened_shapes(shapes:Sequence[Sequence[int]]):
    for s in shapes:
        s = np.prod(s)
        yield int(s)
