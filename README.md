DropTheBeat
===========

[![Build Status](https://travis-ci.org/jacebrowning/dropthebeat.png?branch=master)](https://travis-ci.org/jacebrowning/dropthebeat)
[![Coverage Status](https://coveralls.io/repos/jacebrowning/dropthebeat/badge.png?branch=master)](https://coveralls.io/r/jacebrowning/dropthebeat?branch=master)
[![PyPI Version](https://badge.fury.io/py/DropTheBeat.png)](http://badge.fury.io/py/DropTheBeat)

Music sharing using Dropbox.


Features
--------

* Recommend songs to friends
* Get a list of songs shared by friends
* Download the songs to your computer

![screenshot](https://raw.github.com/jacebrowning/dropthebeat/master/docs/screenshot.png)



Getting Started
===============

Requirements
------------

* Python 3.3: http://www.python.org/download/releases/3.3.4/#download


Installation
------------

DropTheBeat can be installed with ``pip``:

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


For Contributors
================

Requirements
------------

* GNU Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html


Installation
------------

Create a virtualenv:

    make env

Run the tests:

    make test
    make tests  # includes integration tests

Build the documentation:

    make doc

Run static analysis:

    make pep8
    make pylint
    make check  # pep8 and pylint

Prepare a release:

    make dist  # dry run
    make upload

Launch the GUI:

    make gui
