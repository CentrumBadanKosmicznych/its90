# -*- coding: utf-8 -*-
"""
Created on Fri May  8 00:32:23 2015

@author: pgrudzinski
"""

from setuptools import setup, find_packages

setup(
    name='its90',
    description='resistance and temperature of PRT according to ITS90',
    version='0.1',
    author='Paweł Grudziński',
    author_email='',
    packages=['its90'],
    install_requires=['numpy>=1.9'],
    test_suite='test',
)
