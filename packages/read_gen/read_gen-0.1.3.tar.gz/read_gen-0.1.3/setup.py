#!/usr/bin/env python

from setuptools import setup, find_packages

import io
import os

import read_gen

setup(
    name='read_gen',
    version=read_gen.__version__,
    platforms='any',
    packages=['read_gen'],
    scripts=['bin/readgen'],

    author='Bilal Akil',
    author_email='mail@bilalakil.me',
    description=read_gen.__description__,
    url='http://bitbucket.org/bilalakil/readgen',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
