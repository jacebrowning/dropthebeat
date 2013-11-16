#!/usr/bin/env python

"""
Classes and functions to interact with users.
"""

import os
import socket
import getpass
import shutil
import logging

import yaml

from dtb.song import Song


class User(object):
    """Represents a user directory."""

    PRIVATE = '.dtb'
    INFO = os.path.join(PRIVATE, 'info.yml')
    SETTINGS = os.path.join(PRIVATE, 'settings.yml')
    REQUESTS = os.path.join(PRIVATE, 'requests.yml')
    LIBRARY = os.path.join(PRIVATE, 'library.sqlite3')
    DROPS = os.path.join(PRIVATE, 'drops')

    def __init__(self, path):
        self.path = path
        self.share, self.name = os.path.split(self.path)

    def __str__(self):
        return str(self.path)

    @staticmethod
    def new(share, name):
        """Create a new user in the share location."""
        path = os.path.join(share, name)
        if os.path.exists(path):
            raise EnvironmentError("user already exists: {}".format(path))
        private = os.path.join(path, User.PRIVATE)
        drops = os.path.join(path, User.DROPS)
        # Create directories
        os.makedirs(private)
        os.makedirs(drops)
        # Create info
        with open(os.path.join(path, User.INFO), 'w') as config:
            info = get_info()
            data = {'computer': info[0],
                    'username': info[1]}
            config.write(yaml.dump(data, default_flow_style=False))
        # Create settings
        with open(os.path.join(path, User.SETTINGS), 'w') as config:
            data = {'downloads': os.path.expanduser('~/Downloads')}
            config.write(yaml.dump(data, default_flow_style=False))
        # Create request
        with open(os.path.join(path, User.REQUESTS), 'w') as requests:
            data = []
            requests.write(yaml.dump(data, default_flow_style=False))
        # Create folders for friends
        friends = [d for d in os.listdir(share) if d != name]
        for friend in friends:
            os.mkdir(os.path.join(path, friend))
            os.mkdir(os.path.join(share, friend, name))
        # Return the new user
        return User(path)

    @property
    def info(self):
        """Get the user's information."""
        computer = username = None
        path = os.path.join(self.path, User.INFO)
        with open(path, 'r') as config:
            data = yaml.load(config.read())
            if data:
                computer = data.get('computer', None)
                username = data.get('username', None)
        return computer, username

    @property
    def downloads(self):
        """Get the user's download path."""
        path = None
        with open(os.path.join(self.path, User.SETTINGS), 'r') as settings:
            data = yaml.load(settings.read())
            if data:
                path = data.get('downloads', None)
        return path

    @property
    def friends(self):
        """Iterate through the user's friends."""
        for name in os.listdir(self.share):
            if name != self.name:
                yield User(os.path.join(self.share, name))

    @property
    def incoming(self):
        """Iterate through the list of incoming songs."""
        logging.debug("looking for incoming songs...")
        for friendname in os.listdir(self.path):
            if friendname != User.PRIVATE:
                friendpath = os.path.join(self.path, friendname)
                for filename in os.listdir(friendpath):
                    filepath = os.path.join(friendpath, filename)
                    yield Song(filepath, self.downloads, friendname)

    @property
    def outgoing(self):
        """Iterate through the list of outgoing songs."""
        logging.debug("looking for outgoing songs...")
        for friend in self.friends:
            for song in friend.incoming:
                if song.friendname == self.name:
                    yield song

    def recommend(self, path, users=None):
        """Recommend a song to a list of users."""
        logging.info("recommending {}...".format(path))
        drops = os.path.join(self.path, User.DROPS)
        song = Song(shutil.copy(path, drops))  # TODO: symlink instead of copy
        for friend in self.friends:
            if not users or friend in users:
                song.link(os.path.join(friend.path, self.name))

    def request(self, song):
        """Request a new song."""
        raise NotImplementedError()

    def delete(self):
        """Delete the user."""
        raise NotImplementedError()


def get_info():
    """Return the current computer name and user name."""
    return socket.gethostname(), getpass.getuser()


def get_current(share):
    """Get the current user based on this computer's information."""
    info = get_info()
    logging.debug("looking for {} in {}...".format(info, share))
    for directory in os.listdir(share):
        path = os.path.join(share, directory)
        user = User(path)
        if user.info == info:
            logging.info("found user: {}".format(user))
            return user

    raise EnvironmentError("{} not found in {}".format(info, share))
