Unix: [![Unix Build Status](http://img.shields.io/travis/jacebrowning/dropthebeat/develop.svg)](https://travis-ci.org/jacebrowning/dropthebeat) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/dropthebeat/develop.svg)](https://ci.appveyor.com/project/jacebrowning/dropthebeat)<br>Metrics: [![Coverage Status](http://img.shields.io/coveralls/jacebrowning/dropthebeat/develop.svg)](https://coveralls.io/r/jacebrowning/dropthebeat) [![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/dropthebeat.svg)](https://scrutinizer-ci.com/g/jacebrowning/dropthebeat/?branch=develop)<br>Usage: [![PyPI Version](http://img.shields.io/pypi/v/DropTheBeat.svg)](https://pypi.python.org/pypi/DropTheBeat) [![PyPI Downloads](http://img.shields.io/pypi/dm/DropTheBeat.svg)](https://pypi.python.org/pypi/DropTheBeat)

# Overview

Recommend songs to your friends and download their shared files to your computer.

## Features

* Recommend songs to your friends
* Get a list of songs shared by your friends
* Download the songs to your computer

![screenshot](https://github.com/jacebrowning/dropthebeat/blob/master/docs/assets/screenshot.png)

# Setup

## Requirements

* Python 3.3+

## Installation

Install DropTheBeat with pip:

```
$ pip install DropTheBeat
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/dropthebeat.git
$ cd dropthebeat
$ python setup.py install
```

## Configuration

1. Create a folder named 'DropTheBeat' in your Dropbox
2. Share this folder with your friends

# Usage

## Graphical Interface

Start the application:

```
$ DropTheBeat
```

## Command-line Interface

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
