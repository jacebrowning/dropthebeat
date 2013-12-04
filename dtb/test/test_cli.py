#!/usr/bin/env python

"""
Tests for the dtb.cli module.
"""

import unittest
from unittest.mock import patch, Mock

import os
import tempfile
import shutil
import logging

import yaml

from dtb.cli import main

from dtb.test import ENV, REASON, FAKESONG

if __name__ == '__main__':
    os.environ[ENV] = '1'


@unittest.skipUnless(os.getenv(ENV), REASON)  # pylint: disable=R0904
class TestCLI(unittest.TestCase):  # pylint: disable=R0904
    """Integration tests for the 'dtb' command-line interface."""

    def setUp(self):
        self.cwd = os.getcwd()
        self.root = tempfile.mkdtemp()
        self.downloads = tempfile.mkdtemp()
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.downloads)
        shutil.rmtree(self.root)

    @staticmethod
    def log(msg):
        """Header for logging."""
        text = '\n\n'
        text += '#' * 79 + '\n'
        text += '# ' + msg + '\n'
        text += '#' * 79 + '\n'
        logging.info(text)

    def set_downloads(self, name):
        """Change the downloads directory for the user."""
        path = os.path.join(self.root, name, '.dtb', 'info.yml')
        with open(path, 'r') as infile:
            text = infile.read()
        data = yaml.load(text)
        data[0]['downloads'] = self.downloads
        text = yaml.dump(data)
        with open(path, 'w') as outfile:
            outfile.write(text)

    def dtb(self, *args):
        """Run the CLI with string arguments."""
        args += ('--root', self.root, '-v')
        logging.info("$ {}".format(' '.join(args)))
        main(args)

    def ls(self, path, filename, expected=True):  # pylint:disable=C0103
        """Display files in a directory and assert a filename exists."""
        logging.info("$ ls {}".format(path))
        filenames = os.listdir(path)
        for fname in filenames:
            logging.info(fname)
        if expected:
            self.assertIn(filename, filenames)
        else:
            self.assertNotIn(filename, filenames)

    def cat(self, path, expected):
        """Assert the contents of a file."""
        with open(path, 'r') as infile:
            actual = infile.read()
        self.assertEqual(expected, actual)

    def test_recommend_download(self):
        """Verify a song can be shared and downloaded."""
        self.log("downloading a shared song")
        # Create users
        self.dtb('--new', 'JaneDoe')
        self.dtb('--new', 'JohnDoe')
        self.dtb('--new', 'JaceBrowning')
        # Modify their download directory
        self.set_downloads('JaneDoe')
        self.set_downloads('JohnDoe')
        self.set_downloads('JaceBrowning')
        # Share a song
        self.dtb('--share', FAKESONG, '--test', 'JaceBrowning')
        # Show the shared song
        self.dtb('--outgoing', '--test', 'JaceBrowning')
        # Download the shared song (1)
        self.dtb('--incoming', '--test', 'JaneDoe')
        self.dtb('--test', 'JaneDoe')
        self.ls(self.downloads, 'FakeSong.mp3')
        os.remove(os.path.join(self.downloads, 'FakeSong.mp3'))
        # Download the shared song (2)
        self.dtb('--incoming', '--test', 'JohnDoe')
        self.dtb('--test', 'JohnDoe')
        self.ls(self.downloads, 'FakeSong.mp3')
        # Show that no more songs are shared
        self.dtb('--outgoing', '--test', 'JaceBrowning')
        # Check the log
        self.ls(self.downloads, 'dtb.log')
        self.cat(os.path.join(self.downloads, 'dtb.log'),
                 "FakeSong.mp3 from JaceBrowning\n"
                 "FakeSong.mp3 from JaceBrowning\n")

    def test_recommend_download_no_log(self):
        """Verify a song can be shared and downloaded."""
        self.log("downloading a shared song without a log")
        # Create users
        self.dtb('--new', 'JaneDoe')
        self.dtb('--new', 'JohnDoe')
        # Modify their download directory
        self.set_downloads('JaneDoe')
        self.set_downloads('JohnDoe')
        # Share a song
        self.dtb('--share', FAKESONG, '--test', 'JaneDoe')
        # Download the shared song
        self.dtb('--no-log', '--test', 'JohnDoe')
        # Check for no long
        self.ls(self.downloads, 'dtb.log', expected=False)

    @patch('time.sleep', Mock(side_effect=KeyboardInterrupt))
    def test_interrupt_daemon(self):
        """Verify the daemon can be interrupted."""
        self.log("interrupting the daemon")
        # Create user
        self.dtb('--new', 'JaceBrowning')
        # Run the daemon
        self.assertIs(None, self.dtb('--daemon'))

    def test_duplicate_users(self):
        """Verify duplicate users cannot be created."""
        self.log("creating a duplicate user")
        # Create user
        self.dtb('--new', 'JaceBrowning')
        # Create user again
        self.assertRaises(SystemExit, self.dtb, '--new', 'JaceBrowning')

    def test_deleting_users(self):
        """Verify users can be deleted."""
        self.log("deleting a user")
        # Create user
        self.dtb('--new', 'JaceBrowning')
        # Delete user
        self.dtb('--delete')

    @patch('dtb.gui.run', Mock(return_value=True))
    def test_launch_gui(self):
        """Verify the GUI can be launched."""
        self.log("launching the GUI")
        # Create user
        self.dtb('--new', 'JaceBrowning')
        # Launch the GUI
        self.dtb('--gui')


@patch('dtb.cli._run', Mock(return_value=True))  # pylint: disable=R0904
class TestLogging(unittest.TestCase):  # pylint: disable=R0904
    """Integration tests for logging levels."""

    def test_verbose_0(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main([]))

    def test_verbose_1(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main(['-v']))

    def test_verbose_2(self):
        """Verify verbose level 2 can be set."""
        self.assertIs(None, main(['-v', '-v']))

    def test_verbose_3(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main(['-v', '-v', '-v']))


if __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    unittest.main()
