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

* Python 3


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
* GNU Make (or Cygwin Make): http://www.gnu.org/software/make/
* Pandoc: http://johnmacfarlane.net/pandoc/
* virtualenv: https://pypi.python.org/pypi/virtualenv

Environment
-----------

    make develop  # creates the virtualenv
    
    make doc  # runs documentation generation 
    make pep8  # runs pep8 analysis
    make pylint  # runs pylint
    make check  # runs all of the above
    
    make test  # runs the unit tests
    make tests  # runs the integration tests
    
    make gui  # launch the GUI from the virtualenv
