import yaml
import json

from pathlib import Path
from .base2 import Inputs


class ReadInputs(Inputs):
    
    def __init__(self, cfg_file:str, data: dict={}):
        super().__init__(data)
        
        self.cfg_file = cfg_file
        
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
        cls.cfg_file = file
        return cls(file, data)


def read_yaml(file:str):
    with open(file, 'r') as handler:
        data = yaml.load(handler, yaml.FullLoader)
    
    return data


def read_json(file:str):
    with open(file, 'r') as handler:
        data = json.load(handler)
    
    return data
