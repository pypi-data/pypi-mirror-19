#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='type_safety',
    package=['type_safety'],
    version='0.4',
    description='python decorators to enable type-safety on python functions, classes, and generators.',
    author='WillBrennan',
    author_email='WillBrennan@users.noreply.github.com',
    url='https://github.com/WillBrennan/type-safety',
    download_url='https://github.com/WillBrennan/type-safety/tarball/0.4',
    keywords=['type-safety', 'type-safe', 'type', 'safe', 'safety', 'functions', 'classes', 'generators'],
    license="MIT",
    install_requires=["pytest"],
    packages=find_packages(exclude=('tests', 'docs')))
