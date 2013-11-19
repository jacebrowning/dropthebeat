#!/usr/bin/env python

"""
Unit tests for the dtb.song module.
"""

import unittest
from unittest.mock import patch, Mock

import os

from dtb.song import Song

from dtb.test import FILES, EMPTY

FAKESONG = os.path.join(FILES, 'FakeSong.mp3')
FAKELINK = os.path.join(FILES, 'abc123.yml')
FAKEFILE = os.path.join(FILES, 'FakeFile.yml')
BROKENLINK = os.path.join(FILES, 'broken.yml')


class TestSong(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the Song class."""  # pylint: disable=C0103,W0212

    def setUp(self):
        self.song_min = Song(FAKESONG)  # TODO: which tests for this object?
        self.song = Song(FAKESONG, downloads=EMPTY, friendname='Jace')
        self.link = Song(FAKELINK, downloads=EMPTY, friendname='Jace')
        self.file = Song(FAKEFILE, downloads=EMPTY, friendname='Jace')
        self.broken = Song(BROKENLINK, downloads=EMPTY, friendname='Jace')

    def tearDown(self):
        for name in os.listdir(EMPTY):
            os.remove(os.path.join(EMPTY, name))

    def test_str(self):
        """Verify a song can be converted to string."""
        self.assertEqual(FAKESONG, str(self.song))

    def test_link(self):
        """Verify a link to a song can be created."""
        self.song.link(EMPTY)
        link = Song(os.path.join(EMPTY,
                                 '1c2b6dab7ed53e4b6fc0f0e5a1043f75.yml'))
        self.assertEqual(link.source, self.song.path)
        self.assertTrue(os.path.isfile(link.path))

    def test_source_song(self):
        """Verify a direct song can be followed."""
        self.assertEqual(self.song.path, self.link.source)

    def test_source_link(self):
        """Verify a link can be followed."""
        self.assertEqual(self.song.path, self.song.source)

    def test_source_file(self):
        """Verify a non-link YAML file can be followed."""
        self.assertEqual(self.file.path, self.file.source)

    @patch('os.remove')
    def test_download_song(self, mock_remove):
        """Verify a song can be downloaded."""
        self.song.download()
        path = os.path.join(EMPTY, 'FakeSong.mp3')
        self.assertTrue(os.path.isfile(path))
        mock_remove.assert_called_once_with(self.song.path)

    @patch('os.remove')
    def test_download_link(self, mock_remove):
        """Verify a linked song can be downloaded."""
        self.link.download()
        path = os.path.join(EMPTY, 'FakeSong.mp3')
        self.assertTrue(os.path.isfile(path))
        mock_remove.assert_called_once_with(self.link.path)

    @patch('os.remove')
    def test_download_broken(self, mock_remove):
        """Verify a broken link cannot be downloaded."""
        self.broken.download()
        self.assertEqual(0, len(os.listdir(EMPTY)))
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
