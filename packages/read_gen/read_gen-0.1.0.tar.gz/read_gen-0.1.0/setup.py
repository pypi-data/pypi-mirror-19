#!/usr/bin/env python

from setuptools import setup, find_packages

import io
import os

import read_gen

readme = None
with io.open('README.md', encoding='utf-8') as f:
    readme=f.read()

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
    long_description=readme,
    license='MIT'
)
