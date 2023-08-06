#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.2'
DESCRIPTION = 'disque client (fork used by dwq)'

setup(
    name='pydisque-dwq',
    version=VERSION,
    description=DESCRIPTION,
    author='ybrs',
    license='MIT',
    url="http://github.com/kaspar030/pydisque",
    author_email='kaspar@schleiser.de',
    packages=['pydisque'],
    install_requires=['redis', 'six'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
