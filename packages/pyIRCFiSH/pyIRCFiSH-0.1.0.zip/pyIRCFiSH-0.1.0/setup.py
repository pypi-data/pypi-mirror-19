#!/usr/bin/env python
from distutils.core import setup

setup(
    name='pyIRCFiSH',
    version='0.1.0',
    author='Brian Sykes',
    author_email='bsykes@bdscomputers.ca',
    packages=['pyircfish'],
    url='http://pypi.python.org/pypi/pyIRCFiSH/',
    license='LICENSE.txt',
    description='Python implementation of the IRC with SSL and FiSH support.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pycrypto >= 2.6.1"
    ],
)
