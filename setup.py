#!/usr/bin/env python

"""
Setup script for Comparable.
"""

from dtb import __project__

import setuptools

setuptools.setup(
    name=__project__,
    version='0.0.0',

    description="Music sharing using Dropbox.",
    url='http://pypi.python.org/pypi/DropTheBeat',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},


    long_description=open('README.rst').read(),
    license='LGPL',

    install_requires=[],
)
