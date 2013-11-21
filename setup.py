#!/usr/bin/env python

"""
Setup script for DropTheBeat.
"""

from dtb import __project__, CLI, GUI

import setuptools

# Touch the README, it will be generated on release
README = 'README.rst'
import os
if not os.path.exists(README):
    open(README, 'wb').close()

setuptools.setup(
    name=__project__,
    version='0.0.1-alpha.1',

    description="Music sharing using Dropbox.",
    url='http://pypi.python.org/pypi/DropTheBeat',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': [CLI + ' = dtb.cli:main',
                                      GUI + ' = dtb.gui:main']},

    long_description=open(README).read(),
    license='LGPL',

    install_requires=["wheel", "PyYAML==3.10", "sqlalchemy==0.8.3"],
)
