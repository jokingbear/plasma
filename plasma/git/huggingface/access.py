import pickle

from typing import NamedTuple
from ..work_dir import WORK_DIR


class User(NamedTuple):
    name:str
    token:str


def login(username:str, token:str):
    user = User(username, token)
    
    global HF_USER 
    HF_USER = user
    with open(f'{WORK_DIR}/user.pkl', 'wb') as handler:
        pickle.dump(user, handler)


def _auto():
    try:
        with open(f'{WORK_DIR}/user.pkl', 'rb') as handler:
            return pickle.load(handler)
    except Exception:
        return None


HF_USER:User|None = _auto()
