DropTheBeat
===========

Recommend songs to your friends and download their shared files to your computer.

[![Build Status](http://img.shields.io/travis/jacebrowning/dropthebeat/master.svg)](https://travis-ci.org/jacebrowning/dropthebeat)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/dropthebeat/master.svg)](https://coveralls.io/r/jacebrowning/dropthebeat)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/dropthebeat.svg)](https://scrutinizer-ci.com/g/jacebrowning/dropthebeat/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/DropTheBeat.svg)](https://pypi.python.org/pypi/DropTheBeat)
[![PyPI Downloads](http://img.shields.io/pypi/dm/DropTheBeat.svg)](https://pypi.python.org/pypi/DropTheBeat)

Features
--------

* Recommend songs to your friends
* Get a list of songs shared by your friends
* Download the songs to your computer

![screenshot](docs/assets/screenshot.png)

Getting Started
===============

Requirements
------------

* Python 3.3+

Installation
------------

DropTheBeat can be installed with pip:

```
$ pip3 install DropTheBeat
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/dropthebeat.git
$ cd dropthebeat
$ python3 setup.py install
```

Initial Setup
-------------

1. Create a folder named 'DropTheBeat' in your Dropbox
2. Share this folder with your friends

Graphical Interface
===================

Start the application:

```
$ DropTheBeat
```

Command-line Interface
======================

Create your user folder:

```
$ dtb --new <"First Last">
```

Recommend a song to friends:

```
$ dtb --share <path/to/a/song>
$ dtb --share <path/to/a/song> --users "John Doe" "Jane Doe"
```

Display recommended songs:

```
$ dtb --incoming
$ dtb --outoing
```

Download recommended songs:

```
$ dtb
$ dtb --daemon
```

Launch the GUI:

```
$ dtb --gui
```

For Contributors
================

Requirements
------------

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

Installation
------------

Create a virtualenv:

```
$ make env
```

Run the tests:

```
$ make test
$ make tests  # includes integration tests
```

Build the documentation:

```
$ make doc
```

Run static analysis:

```
$ make pep8
$ make pep257
$ make pylint
$ make check  # includes all checks
```

Prepare a release:

```
$ make dist  # dry run
$ make upload
```

Launch the GUI:

```
$ make gui
```
