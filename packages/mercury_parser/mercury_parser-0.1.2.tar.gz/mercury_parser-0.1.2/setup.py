#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup

try:
    # Python 3
    from os import dirname
except ImportError:
    # Python 2
    from os.path import dirname

here = os.path.abspath(dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = [
    'requests',
    'maya'
]

setup(
    name='mercury_parser',
    version='0.1.2',
    description='Mercury Web Parser API Client.',
    long_description= '\n' + read('README.rst'),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/mercury-parser',
    py_modules=['mercury_parser'],
    install_requires=required,
    license='MIT',
    classifiers=(

    ),
)
