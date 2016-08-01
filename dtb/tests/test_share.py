#!/usr/bin/env python

"""Unit tests for the dtb.share module."""

import unittest
from unittest.mock import patch, Mock

import os
import tempfile
import shutil

from dtb import share

from dtb.tests import FILES


class TestFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the sharing functions class."""  # pylint: disable=C0103,W0212

    def test_find_dropbox(self):
        """Verify a sharing folder can be found for Dropbox."""
        temp = tempfile.mkdtemp()
        os.makedirs(os.path.join(temp, 'Dropbox', 'DropTheBeat'))
        try:
            path = share.find(temp)
            self.assertTrue(os.path.isdir(path))
        finally:
            shutil.rmtree(temp)

    def test_find_dropbox_personal(self):
        """Verify a sharing folder can be found for Dropbox (Personal)."""
        temp = tempfile.mkdtemp()
        os.makedirs(os.path.join(temp, 'Dropbox (Personal)', 'DropTheBeat'))
        try:
            path = share.find(temp)
            self.assertTrue(os.path.isdir(path))
        finally:
            shutil.rmtree(temp)

    @patch('dtb.share.SHARE_DEPTH', 2)
    def test_find_depth(self):
        """Verify a sharing folder is not found below the depth."""
        temp = tempfile.mkdtemp()
        os.makedirs(os.path.join(temp, 'Dropbox', 'a', 'b', 'DropTheBeat'))
        try:
            self.assertRaises(OSError, share.find, temp)
        finally:
            shutil.rmtree(temp)

    @patch('os.path.isdir', Mock(return_value=False))
    def test_find_no_home(self):
        """Verify an error occurs when no home directory is found."""
        self.assertRaises(EnvironmentError, share.find)

    def test_find_no_share(self):
        """Verify an error occurs when no home directory is found."""
        self.assertRaises(EnvironmentError, share.find, FILES)


if __name__ == '__main__':
    unittest.main()
