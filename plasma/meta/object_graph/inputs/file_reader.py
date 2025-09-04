import yaml
import json

from .base import Inputs
from pathlib import Path


class ReadInputs(Inputs):
    
    @classmethod
    def read(cls, file:str):
        path = Path(file)
        if 'yaml' in path.suffix:
            data = read_yaml(path)
        elif 'json' in path.suffix:
            data = read_json(path)
        
        return cls(data)


def read_yaml(file:str):
    with open(file, 'r') as handler:
        data = yaml.load(handler, yaml.FullLoader)
    
    return data


def read_json(file:str):
    with open(file, 'r') as handler:
        data = json.load(handler)
    
    return data