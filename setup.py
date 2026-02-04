import re
import os

from setuptools import setup
from pathlib import Path

packages = [re.sub(r'\\|\/', '.', str(p.parent)) for p in Path('plasma').rglob('__init__.py')]

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"

with open(requirement_path) as f:
        install_requires = f.readlines()

setup(
    name='plasma',
    version='4.4.6a2',
    packages=[*packages],
    license='MIT',
    author='jokingbear',
    install_requires=install_requires
)