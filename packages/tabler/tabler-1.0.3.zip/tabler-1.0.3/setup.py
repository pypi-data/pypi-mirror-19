#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='tabler',
    version='1.0.03',
    description='Simple interface for tabulated data and .csv files',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://tabler.lukeshiner.com',
    keywords=['table', 'csv', 'simple'],
    install_requires=['requests'],
    packages=find_packages(),
    )
