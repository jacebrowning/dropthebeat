#!/usr/bin/env python

"""
Unit tests for the dtb.user module.
"""

import unittest
from unittest.mock import patch, Mock, call

import os
import tempfile
import shutil

from dtb.user import User, get_current

from dtb.test import FILES

FAKESONG = os.path.join(FILES, 'FakeSong.mp3')
FAKELINK = os.path.join(FILES, 'abc123.yml')
FAKEFILE = os.path.join(FILES, 'FakeFile.yml')
BROKENLINK = os.path.join(FILES, 'broken.yml')


class MockSong(Mock):
    """Mock Song class."""

    link = Mock()


class TestUser(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the User class."""  # pylint: disable=C0103,W0212

    INFOS = [('PC', 'MrTemp'),
             ('PC', 'MrTemp2'),
             ('PC', 'MrTemp3')]

    @classmethod
    @patch('dtb.user.get_info', Mock(side_effect=INFOS))
    def setUpClass(cls):
        cls.root = tempfile.mkdtemp()
        cls.downloads = tempfile.mkdtemp()
        cls.name = 'TempUser'
        cls.user = User.new(cls.root, cls.name, downloads=cls.downloads)
        cls.user2 = User.new(cls.root, cls.name + '2')
        cls.user3 = User.new(cls.root, cls.name + '3')
        with open(os.path.join(cls.root, 'desktop.ini'), 'w'):
            pass  # create a "junk" file in the share directory

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root)
        shutil.rmtree(cls.downloads)

    def test_new_duplicate(self):
        """Verify a user cannot be created twice."""
        self.assertRaises(EnvironmentError, User.new, self.root, self.name)

    def test_str(self):
        """Verify a user can be converted to a string."""
        text = str(os.path.join(self.root, self.name))
        self.assertEqual(text, str(self.user))

    def test_cmp(self):
        """Verify users can be compared."""
        self.assertEqual(self.user, self.user)
        self.assertNotEqual(self.user, self.user2)

    def test_name(self):
        """Verify a user's name is correct."""
        self.assertEqual(self.name, self.user.name)

    def test_root(self):
        """Verify a user's root path is correct."""
        self.assertEqual(self.root, self.user.root)

    def test_path_private(self):
        """Verify a user's private path is correct."""
        path = os.path.join(self.root, self.name, '.dtb')
        self.assertEqual(path, self.user.path_private)
        self.assertTrue(os.path.isdir(path))

    def test_path_drops(self):
        """Verify a user's drops path is correct."""
        path = os.path.join(self.root, self.name, '.dtb', 'drops')
        self.assertEqual(path, self.user.path_drops)
        self.assertTrue(os.path.isdir(path))

    def test_path_info(self):
        """Verify a user's info path is correct."""
        path = os.path.join(self.root, self.name, '.dtb', 'info.yml')
        self.assertEqual(path, self.user.path_info)
        self.assertTrue(os.path.isfile(path))

    def test_path_library(self):
        """Verify a user's library path is correct."""
        path = os.path.join(self.root, self.name, '.dtb', 'library.sqlite3')
        self.assertEqual(path, self.user.path_library)
        # TODO: add this test when library support is added
        # self.assertTrue(os.path.isfile(path))

    def test_path_reuests(self):
        """Verify a user's requests path is correct."""
        path = os.path.join(self.root, self.name, '.dtb', 'requests.yml')
        self.assertEqual(path, self.user.path_requests)
        self.assertTrue(os.path.isfile(path))

    def test_path_settings(self):
        """Verify a user's settings path is correct."""
        path = os.path.join(self.root, self.name, '.dtb', 'settings.yml')
        self.assertEqual(path, self.user.path_settings)
        self.assertTrue(os.path.isfile(path))

    def test_path_downloads(self):
        """Verify a user's downloads path is correct."""
        path = self.downloads
        self.assertEqual(path, self.user.path_downloads)
        self.assertTrue(os.path.isdir(path))

    def test_path_downloads_set(self):
        """Verify a user's downloads path can be set."""
        self.user.path_downloads = '_downloads'
        self.assertEqual('_downloads', self.user.path_downloads)

    def test_info(self):
        """Verify a user's info is correct."""
        self.assertEqual(('PC', 'MrTemp'), self.user.info)

    def test_friends(self):
        """Verify a user's friends are correct."""
        friends = list(self.user.friends)
        self.assertEqual(2, len(friends))
        self.assertIsInstance(friends[0], User)

    def test_incoming(self):
        """Verify a user's incoming songs are correct."""
        path = os.path.join(self.user.path, 'TempUser2', '_a_song')
        open(path, 'w').close()  # touch the file
        try:
            songs = list(self.user.incoming)
            self.assertEqual(1, len(songs))
            self.assertEqual('TempUser2', songs[0].friendname)
        finally:
            os.remove(path)

    def test_incoming_zero(self):
        """Verify there can be zero incoming songs."""
        songs = list(self.user.incoming)
        self.assertEqual(0, len(songs))

    def test_outgoing(self):
        """Verify a user's outgoing songs are correct."""
        path = os.path.join(self.user2.path, self.name, '_a_song')
        open(path, 'w').close()  # touch the file
        try:
            songs = list(self.user.outgoing)
            self.assertEqual(1, len(songs))
            self.assertEqual(self.user2.name, songs[0].friendname)
        finally:
            os.remove(path)

    def test_outgoing_zero(self):
        """Verify there can be zero incoming songs."""
        songs = list(self.user.outgoing)
        self.assertEqual(0, len(songs))

    def test_cleanup(self):
        """Verify a user's directory can be cleaned."""
        path = os.path.join(self.user.path_drops, '_a_song')
        path2 = os.path.join(self.user2.path, self.name, '_a_song2')
        open(path, 'w').close()  # touch the file
        open(path2, 'w').close()  # touch the file
        try:
            self.assertEqual(1, len(os.listdir(self.user.path_drops)))
            self.user.cleanup()
            self.assertEqual(0, len(os.listdir(self.user.path_drops)))
        finally:
            os.remove(path2)

    @patch('dtb.user.Song', MockSong)
    def test_recommend(self,):
        """Verify a user can recommend a song."""
        self.user.recommend(FAKESONG)
        path2 = os.path.join(self.user2.path, self.name)
        path3 = os.path.join(self.user3.path, self.name)
        self.assertEqual(2, len(MockSong.link.call_args_list))
        self.assertIn(call(path2), MockSong.link.call_args_list)
        self.assertIn(call(path3), MockSong.link.call_args_list)

    def test_request(self):
        """Verify a user can request a song."""
        # TODO: update this test when feature implemented
        self.assertRaises(NotImplementedError, self.user.request, None)

    def test_check(self):
        """Verify a user can be checked."""
        self.user.check()

    def test_check_file_error(self):
        """Verify a user fails the check with a missing files."""
        user = User.new(self.root, '_temp')
        try:
            os.remove(user.path_info)
            self.assertRaises(ValueError, user.check)
        finally:
            user.delete()

    def test_check_folder_error(self):
        """Verify a user fails the check with a missing folders."""
        user = User.new(self.root, '_temp')
        try:
            shutil.rmtree(user.path_drops)
            self.assertRaises(ValueError, user.check)
        finally:
            user.delete()

    def test_delete(self):
        """Verify a user can be deleted."""
        user = User.new(self.root, '_temp')
        self.assertTrue(os.path.isdir(user.path))
        user.delete()
        self.assertFalse(os.path.isdir(user.path))

    @patch('dtb.user.get_info', Mock(return_value=INFOS[0]))
    def test_get_current(self):
        """Verify the current user can be retrieved."""
        user = get_current(self.root)
        self.assertEqual(self.user, user)

    def test_get_current_error(self):
        """Verify an error occurs when the user cannot be found."""
        self.assertRaises(EnvironmentError, get_current, self.root)


if __name__ == '__main__':
    unittest.main()
