#!/usr/bin/env python
from setuptools import setup, find_packages

import tahoe_sites

setup(
    name='tahoe-sites',
    version=tahoe_sites.__version__,
    description='Site and organization multi-tenancy management for Appsembler Tahoe',
    author='Appsembler',
    url='https://github.com/appsembler/tahoe-sites',
    license='MIT License - Copyright (c) 2022 Appsembler',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'License :: MIT License - Copyright (c) 2022 Appsembler',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=['tests']),
)
