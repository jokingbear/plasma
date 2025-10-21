import importlib
import inspect
import os

from .module_hub import ModuleHub
from pathlib import Path
from .entry_factory import get_module_entry


def import_module(path, verbose=True):
    """
    get enty point of a hub folder
    :param path: path to python module
    :param verbose: be verbose in importing module
    :return: HubEntries
    """
    path = Path(path)
    module = ModuleHub(path.parent, path.name.replace(".py", ""))

    if verbose:
        print(f'finished importing {path}')

    return module


def load_entry(cfg: dict):
    """
    load an entry from a module
    Args:
        cfg: config dict, must have key path
    Returns:

    """
    if 'path' not in cfg:
        raise AttributeError('there is no path in config file')

    path = cfg['path']
    name = cfg.get('name', None)

    inspector = import_module(path)

    if isinstance(name, str):
        return inspector[name]
    elif get_module_entry(inspector.module.__name__) is not None:
        return get_module_entry(inspector.module.__name__)
    else:
        raise AttributeError(f'Cant find entry point of module {path}, either add an entry decorator or specified'
                             f'entry method/class in cfg name')


def mass_import(pattern):
    caller = inspect.stack()[1][0]
    caller = inspect.getmodule(caller)

    path = Path(caller.__file__)
    parent_path = path.parent
    if not os.path.exists(f'{parent_path}/__init__.py'):
        raise RuntimeError('mass_import can only be used in packaged folder with __init__ file')
    
    for p in parent_path.glob(pattern):
        module_name = p.name.replace('.py', '')
        importlib.import_module(f'.{module_name}', caller.__package__)
