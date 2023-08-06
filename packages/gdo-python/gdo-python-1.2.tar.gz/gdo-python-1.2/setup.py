#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='gdo-python',
    version='1.2',
    description='Utility for building applications with gdo in python(3)',
    author='Sebastian Jordan',
    author_email='jordan@schneevonmorgen.com',
    url='https://github.com/seppeljordan/gdo-python',
    package_dir = {'': 'src'},
    packages = ['gdo'],
    install_requires = [
        'Jinja2',
    ]
)
