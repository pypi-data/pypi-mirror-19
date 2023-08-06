#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='velbot',
    version='1.0',
    description='A HTTP Based Slack Bot Written in Python.',
    author='Sanjit Menon',
    author_email='sanjimenon@yahoo.com',
    url='https://github.com/sanjimenon/python-velbot',
    packages=find_packages(),
    entry_points={'console_scripts': ['velbot=velbot.bin.run_velbot:main']},
    install_requires=[
        'pyyaml>=3, <4',
        'Flask',
        'slackclient>=1, <2'
    ]
 )

