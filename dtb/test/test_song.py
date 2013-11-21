#!/usr/bin/env python

"""
Unit tests for the dtb.song module.
"""

import unittest
from unittest.mock import patch, Mock

import os
import tempfile
import shutil

from dtb.song import Song

from dtb.test import EMPTY
from dtb.test import FAKESONG, FAKELINK, FAKEFILE, BADFAKEFILE, BROKENLINK




class TestSong(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the Song class."""  # pylint: disable=C0103,W0212

    def setUp(self):
        self.temp = tempfile.mkdtemp()
        self.song = Song(FAKESONG, downloads=self.temp, friendname='Jace')
        self.link = Song(FAKELINK, downloads=self.temp, friendname='Jace')
        self.file = Song(FAKEFILE, downloads=self.temp, friendname='Jace')
        self.bad = Song(BADFAKEFILE, downloads=self.temp, friendname='Jace')
        self.broken = Song(BROKENLINK, downloads=self.temp, friendname='Jace')

    def tearDown(self):
        shutil.rmtree(self.temp)
        for name in os.listdir(EMPTY):
            if name != '.gitignore':
                os.remove(os.path.join(EMPTY, name))

    def test_str(self):
        """Verify a song can be converted to string."""
        self.assertEqual(FAKESONG, str(self.song))

    def test_in_string(self):
        """Verify an incoming song can be presented."""
        text = "FakeSong.mp3 (from Jace)"
        self.assertEqual(text, self.song.in_string)

    def test_out_string(self):
        """Verify an outgoing song can be presented."""
        text = "FakeSong.mp3 (to Jace)"
        self.assertEqual(text, self.song.out_string)

    def test_link(self):
        """Verify a link to a song can be created."""
        self.song.link(EMPTY)
        filename = [f for f in os.listdir(EMPTY) if f.endswith('.yml')][0]
        link = Song(os.path.join(EMPTY, filename))
        self.assertEqual(link.source, self.song.path)
        self.assertTrue(os.path.isfile(link.path))

    def test_link_missing_directory(self):
        """Verify a link can be created even when the directory is gone."""
        temp = tempfile.mkdtemp()
        shutil.rmtree(temp)
        self.song.link(temp)

    def test_source_song(self):
        """Verify a direct song can be followed."""
        self.assertEqual(self.song.path, self.link.source)

    def test_source_link(self):
        """Verify a link can be followed."""
        self.assertEqual(self.song.path, self.song.source)

    def test_source_file(self):
        """Verify a non-link YAML file can be followed."""
        self.assertEqual(self.file.path, self.file.source)

    def test_source_file_bad(self):
        """Verify a non-link invalid YAML is handled."""
        self.assertEqual(self.bad.path, self.bad.source)

    @patch('os.remove')
    def test_download_song(self, mock_remove):
        """Verify a song can be downloaded."""
        self.song.download()
        path = os.path.join(self.temp, 'FakeSong.mp3')
        self.assertTrue(os.path.isfile(path))
        mock_remove.assert_called_once_with(self.song.path)

    @patch('os.remove')
    def test_download_link(self, mock_remove):
        """Verify a linked song can be downloaded."""
        self.link.download()
        path = os.path.join(self.temp, 'FakeSong.mp3')
        self.assertTrue(os.path.isfile(path))
        mock_remove.assert_called_once_with(self.link.path)

    @patch('os.remove')
    def test_download_broken(self, mock_remove):
        """Verify a broken link cannot be downloaded."""
        self.broken.download()
        self.assertEqual(0, len(os.listdir(self.temp)))
        mock_remove.assert_called_once_with(self.broken.path)

    @patch('os.remove', Mock(side_effect=IOError))
    def test_download_error(self):
        """Verify errors are caught while downloading."""
        self.song.download()

    @patch('os.remove')
    def test_ignore(self, mock_remove):
        """Verify a song can be ignored."""
        self.song.ignore()
        mock_remove.assert_called_once_with(self.song.path)


if __name__ == '__main__':
    unittest.main()
