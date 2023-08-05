#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.0.7'

setup(
    name='virtualhermit',
    version=version,
    description='virtualhermit checks your newsfeed before you waste time on it.',
    author='Lakshay Kalbhor',
    author_email='lakshaykalbhor@gmail.com',
    license='MIT',
    keywords=['facebook', 'git', 'github', 'command line', 'cli', 'hermit'],
    url='http://github.com/lakshaykalbhor/virtualhermit',
    packages=['src'],
    install_requires=[
    'requests',
    'colorama',
    'argparse',
    ],
    entry_points={
        'console_scripts': [
            'virtualhermit=src.virtualhermit:main'
        ],
    }
)