DropTheBeat
===========

Music sharing using Dropbox.

Features
--------

* Recommend songs to friends
* Get a list of songs shared by friends
* Download the songs to your computer



Getting Started
===============

Requirements
------------

* Python 3: http://www.python.org/download/releases/3.3.3/#download


Installation
------------

DropTheBeat can be installed with ``pip`` or ``easy_install``:

    pip install DropTheBeat

Or directly from the source code:

    python setup.py install


Initial Setup
-------------

1. Create a folder named 'DropTheBeat' in your Dropbox
2. Share this folder with your friends


Graphical Interface
===================

Start the app:

    DropTheBeat


Command-line Inteface
=====================

Create your user folder:

    dtb --new <FirstLast>

Recommend a song to friends:

    dtb --share <path/to/a/song>
    dtb --share <path/to/a/song> --users JohnDoe JaneDoe

Display recommended songs:

    dtb --incoming
    dtb --outoing

Download recommended songs:

    dtb
    dtb --daemon

Launch the GUI:

    dtb --gui


For Developers
==============

Requirements
------------
* Python 3: http://www.python.org/download/releases/3.3.3/#download
* Cygwin Make (Windows): http://cygwin.com/install.html
* GNU Make (non-Windows): http://www.gnu.org/software/make/
* Pandoc: http://johnmacfarlane.net/pandoc/
* virtualenv: https://pypi.python.org/pypi/virtualenv

Environment
-----------

Create a virtualenv:

    make develop
    
Run static analysis:

    make doc
    make pep8
    make pylint
    make check  # all of the above
    
Run the tests:
    
    make test
    make tests  # includes integration tests
    
Launch the GUI from the virtualenv:
    
    make gui  # sets TCL_LIBRARY on Windows
