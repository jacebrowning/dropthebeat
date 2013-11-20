DropTheBeat
===========

Music sharing using Dropbox.

Features
--------

* Recommend songs to friends
* Get a list of songs recommended by friends
* Ignore or download the songs to your computer



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


Command-line Inteface
---------------------

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


Graphical Interface
-------------------

Start the app:

    DropTheBeat



Development
===========

Requirements
------------
* GNU Make (or Cygwin Make): http://www.gnu.org/software/make/
* Pandoc: http://johnmacfarlane.net/pandoc/
* virtualenv: https://pypi.python.org/pypi/virtualenv
