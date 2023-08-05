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
    url='http://bitbucket.org/bilalakil/read-gen',
    license='MIT'
)
