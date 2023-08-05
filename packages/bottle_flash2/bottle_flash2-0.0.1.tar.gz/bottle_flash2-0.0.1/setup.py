#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="bottle_flash2",
    version='0.0.1',
    url='https://github.com/shinshin86/bottle-flash2',
    py_modules=["bottle_flash2"],
    author='shinshin86',
    author_email='beagles1986@gmail.com',
    maintainer='shinshin86',
    maintainer_email='beagles1986@gmail.com',
    description='flash plugin for bottle',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        "bottle",
    ],
    license="MIT",
    classifiers=[
        'Framework :: Bottle',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
)
