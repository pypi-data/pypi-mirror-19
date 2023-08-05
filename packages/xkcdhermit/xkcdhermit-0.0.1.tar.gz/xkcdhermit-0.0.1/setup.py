#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='xkcdhermit',
    version=version,
    description='xkcdhermit replies to everything with an xkcd comic.',
    author='Lakshay Kalbhor',
    author_email='lakshaykalbhor@gmail.com',
    license='MIT',
    keywords=['xkcd', 'git', 'github', 'command line', 'cli', 'hermit'],
    url='http://github.com/lakshaykalbhor/xkcdhermit',
    packages=['src'],
    install_requires=[
    'requests',
    'colorama',
    'argparse',
    ],
    entry_points={
        'console_scripts': [
            'xkcdhermit=src.xkcdhermit:main'
        ],
    }
)
