#!/usr/bin/env python3
from setuptools import setup
with open('version.txt', 'r') as version_file:
    version = version_file.read().strip()

setup(
        version = version, 
        name='cars_api',
        packages=['cars_api'],
        include_package_data=True,
        install_requires=[
            'flask',
        ],
)

