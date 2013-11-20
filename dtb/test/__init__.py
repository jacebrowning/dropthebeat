#!/usr/bin/env python

"""
Tests for the dtb package.
"""

import os

DIR = os.path.dirname(__file__)
FILES = os.path.join(DIR, 'files')
EMPTY = os.path.join(FILES, 'empty')

FAKESONG = os.path.join(FILES, 'FakeSong.mp3')
FAKELINK = os.path.join(FILES, 'abc123.yml')
FAKEFILE = os.path.join(FILES, 'FakeFile.yml')
BADFAKEFILE = os.path.join(FILES, 'bad.yml')
BROKENLINK = os.path.join(FILES, 'broken.yml')

ENV = 'TEST_INTEGRATION'  # environment variable to enable integration tests
REASON = "'{0}' variable not set".format(ENV)
