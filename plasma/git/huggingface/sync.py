import os
import shutil
import subprocess
import re

from .access import HF_USER
from ..work_dir import WORK_DIR
from ...meta import import_module


def download_module(repo_id: str):
    match = re.search(r'([^@]+)(@.+){0,1}', repo_id)
    assert match is not None, 'repo_id does not follow any known patterns'
    assert HF_USER is not None, 'no authorization, please login'
    
    repo = match.group(1)
    path = f'{WORK_DIR}/{repo}'
    if os.path.exists(repo):
        shutil.rmtree(path)
    
    process = subprocess.run([
        'git',
        'clone',
        f'https://{HF_USER.name}:{HF_USER.token}@huggingface.co/{repo_id}',
        path
    ])
    print(process.stdout)

    return import_module(path)
