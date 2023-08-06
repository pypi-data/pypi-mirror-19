#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: DmytryiStriletskyi
@contact: dmytryi.striletskyi@gmail.com
@license: MIT License
Copyright (C) 2017
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='DouAPI',
    version='1.0.0',
    author='DmytryiStriletskyi',
    author_email='dmytryi.striletskyi@gmail.com',
    url='https://github.com/DmytryiStriletskyi/DouAPI',
    description='Dou API wrapper',
    download_url='https://github.com/DmytryiStriletskyi/DouAPI/archive/master.zip',
    license='MIT',

    packages=['dou'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ]
)
