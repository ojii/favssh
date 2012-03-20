#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from favssh import __version__

INSTALL_REQUIRES = []

try:
    import argparse
except ImportError:
    INSTALL_REQUIRES.append('argparse')

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development',
]

setup(
    name='favssh',
    version=__version__,
    description='A command line tool to manipulate ssh config files',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    url='https://github.com/ojii/favssh/',
    packages=['favssh'],
    license='BSD',
    platforms=['OS Independent'],
    install_requires=INSTALL_REQUIRES,
    entry_points="""
    [console_scripts]
    favssh = favssh.main:main
    """,
)
