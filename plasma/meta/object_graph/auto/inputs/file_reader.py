import yaml
import json
import sched

from pathlib import Path
from .base2 import Inputs


class ReadInputs(Inputs):
    
    @classmethod
    def read(cls, file:str):
        path = Path(file)
        if 'yaml' in path.suffix:
            data = read_yaml(path) # type:ignore
        elif 'json' in path.suffix: 
            data = read_json(path) #type:ignore
        else:
            raise NotImplementedError(
                f'no reader implemented for file type {path.suffix}'
            )
        
        return cls(data)
    
    @classmethod
    def bind(cls, file:str, refresh_interval:float):
        args = cls.read(file)
        
        scheduler = sched.scheduler()
        def reload():
            new_args = cls.read(file)
            args.__setstate__(new_args.__getstate__()) # type:ignore - copy attribute
            scheduler.enter(refresh_interval, 0, reload)
        
        scheduler.enter(refresh_interval, 0, reload)
        return args


def read_yaml(file:str):
    with open(file, 'r') as handler:
        data = yaml.load(handler, yaml.FullLoader)
    
    return data


def read_json(file:str):
    with open(file, 'r') as handler:
        data = json.load(handler)
    
    return data
