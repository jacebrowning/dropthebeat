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
    version='0.0.6',

    description="Music sharing using Dropbox.",
    url='http://github.com/jacebrowning/dropthebeat',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': [CLI + ' = dtb.cli:main',
                                      GUI + ' = dtb.gui:main']},

    long_description=open(README).read(),
    license='LGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',  # pylint: disable=C0301
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Topic :: Communications :: File Sharing',
        'Topic :: Multimedia :: Sound/Audio',
    ],

    install_requires=["PyYAML==3.10"],
)
