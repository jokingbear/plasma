import re

from setuptools import setup
from pathlib import Path

packages = [re.sub(r'\\|\/', '.', str(p.parent)) for p in Path('plasma').rglob('__init__.py')]

with open('requirements.txt', 'r') as handler:
    requirements = handler.readlines()

setup(
    name='plasma',
    version='2.2.2post0',
    packages=['plasma', *packages],
    url='https://github.com/jokingbear/research-idea',
    license='MIT',
    author='jokingbear',
    install_requires=requirements
)
