#!/usr/bin/env python

"""
Unit tests for the dtb.share module.
"""

import unittest
from unittest.mock import patch, Mock

import os

from dtb import share

from dtb.test import FILES


class TestFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the sharing functions class."""  # pylint: disable=C0103,W0212

    def test_find(self):
        """Verify a sharing folder can be found."""
        path = share.find()
        self.assertTrue(os.path.isdir(path))

    @patch('os.path.isdir', Mock(return_value=False))
    def test_find_no_home(self):
        """Verify an error occurs when no home directory is found."""
        self.assertRaises(EnvironmentError, share.find)

    def test_find_no_share(self):
        """Verify an error occurs when no home directory is found."""
        self.assertRaises(EnvironmentError, share.find, FILES)


if __name__ == '__main__':
    unittest.main()