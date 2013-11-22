#!/usr/bin/env python

"""
Tests for the dtb.cli module.
"""

import unittest
from unittest.mock import patch, Mock

import os
import sys
import imp
import logging

from dtb import gui

from dtb.test import ENV, REASON

if __name__ == '__main__':
    os.environ[ENV] = '1'


@unittest.skipUnless(os.getenv(ENV), REASON)  # pylint: disable=R0904
class TestGUI(unittest.TestCase):  # pylint: disable=R0904
    """Integration tests for the 'DropTheBeat' graphical interface."""

    @patch('dtb.gui.run', Mock(side_effect=KeyboardInterrupt))
    def test_interrupt(self):
        """Verify the GUI can be interrupted."""
        self.assertIs(None, gui.main([]))

    @patch('dtb.gui.run', Mock(return_value=False))
    def test_exit(self):
        """Verify the GUI can exit on error."""
        self.assertRaises(SystemExit, gui.main, [])


class TestImport(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for importing the GUI module."""

    def test_import(self):
        """Verify tkinter import errors are handled."""
        sys.modules['tkinter'] = Mock(side_effect=ImportError)
        imp.reload(gui)
        self.assertFalse(gui.run(Mock()))
        self.assertIsInstance(gui.tk, Mock)


@patch('dtb.gui.run', Mock(return_value=True))  # pylint: disable=R0904
class TestLogging(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for logging levels."""

    def test_verbose_0(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, gui.main([]))

    def test_verbose_1(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, gui.main(['-v']))


if __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    unittest.main()
