#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    description = f.read()

install_requires = []

setup(
    name='36-chambers',
    version='0.0.1',
    description='Python Library for Binary Ninja',
    long_description=long_description,
    author='Mike Goffin',
    author_email='mgoffin@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='binary ninja 36 chambers',
    url='https://www.github.com/mgoffin/36-chambers',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=install_requires,
    scripts=[],
)
