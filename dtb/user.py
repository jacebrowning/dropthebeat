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

    def __init__(self, path, _check=True):
        self.path = path
        if _check:
            self.check()

    def __str__(self):
        return str(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def new(root, name, downloads=None):
        """Create a new user in the share location.
        @param share: path to root of sharing directory
        @param name: name of user's sharing folder
        @param downloads: path to user's downloads directory

        @return: new User
        """
        logging.debug("creating user '{}'...".format(name))
        path = os.path.join(root, name)
        if os.path.exists(path):
            raise EnvironmentError("user already exists: {}".format(path))
        downloads = downloads or os.path.expanduser('~/Downloads')
        # Create a new user
        user = User(path, _check=False)
        # Create directories
        os.makedirs(user.path_private)
        os.makedirs(user.path_drops)
        # Create info
        with open(user.path_info, 'w') as outfile:
            info = get_info()
            data = {'computer': info[0],
                    'username': info[1]}
            text = yaml.dump(data, default_flow_style=False)
            outfile.write(text)
        # Create settings
        with open(user.path_settings, 'w') as outfile:
            data = {'downloads': downloads}
            text = yaml.dump(data, default_flow_style=False)
            outfile.write(text)
        # Create requests
        with open(user.path_requests, 'w') as outfile:
            data = []
            text = yaml.dump(data, default_flow_style=False)
            outfile.write(text)
        # Create folders for friends
        for name in os.listdir(root):
            friendpath = os.path.join(root, name)
            if name != user.name and os.path.isdir(friendpath):
                os.mkdir(os.path.join(user.path, name))
                os.mkdir(os.path.join(friendpath, user.name))
        # Return the new user
        logging.info("created user: {}".format(user))
        user.check()
        return user

    ### properties based on path #############################################

    @property
    def name(self):
        """Get the name of the user's folder."""
        return os.path.split(self.path)[1]

    @property
    def root(self):
        """Get the path to root of the sharing directory."""
        return os.path.split(self.path)[0]

    @property
    def path_private(self):
        """Get the path to the user's private directory."""
        return os.path.join(self.path, User.PRIVATE)

    @property
    def path_drops(self):
        """Get the path to the user's drops directory."""
        return os.path.join(self.path, User.DROPS)

    @property
    def path_info(self):
        """Get the path to the user's information file."""
        return os.path.join(self.path, User.INFO)

    @property
    def path_library(self):
        """Get the path to the user's library file."""
        return os.path.join(self.path, User.LIBRARY)

    @property
    def path_requests(self):
        """Get the path to the user's requests file."""
        return os.path.join(self.path, User.REQUESTS)

    @property
    def path_settings(self):
        """Get the path to the user's requests file."""
        return os.path.join(self.path, User.SETTINGS)

    ### properties based on files ############################################

    @property
    def info(self):
        """Get the user's information."""
        computer = username = None
        with open(self.path_info, 'r') as config:
            data = yaml.load(config.read())
            if data:
                computer = data.get('computer', None)
                username = data.get('username', None)
        return computer, username

    @property
    def path_downloads(self):
        """Get the user's download path."""
        path = None
        with open(self.path_settings, 'r') as settings:
            data = yaml.load(settings.read())
            if data:
                path = data.get('downloads', None)
        return path

    @path_downloads.setter
    def path_downloads(self, path):
        """Set the user's download path."""
        # TODO: refactor all into one common reader and writer
        with open(self.path_settings, 'r') as settings:
            text = settings.read()
        data = yaml.load(text)
        data['downloads'] = path
        text = yaml.dump(data)
        with open(self.path_settings, 'w') as settings:
            settings.write(text)

    @property
    def friends(self):
        """Iterate through the user's friends."""
        for directory in os.listdir(self.root):
            try:
                user = User(os.path.join(self.root, directory))
            except ValueError as err:
                logging.debug("invalid user: {}".format(err))
            else:
                if user.name != self.name:
                    yield user

    @property
    def incoming(self):
        """Iterate through the list of incoming songs."""
        found = False
        logging.debug("looking for incoming songs ({})...".format(self.name))
        for friendname in os.listdir(self.path):
            if friendname != User.PRIVATE:
                friendpath = os.path.join(self.path, friendname)
                for filename in os.listdir(friendpath):
                    filepath = os.path.join(friendpath, filename)
                    song = Song(filepath, self.path_downloads, friendname)
                    found = True
                    logging.debug("incoming: {}".format(song))
                    yield song
        if not found:
            logging.debug("no incoming songs ({})".format(self.name))

    @property
    def outgoing(self):
        """Iterate through the list of outgoing songs."""
        found = False
        logging.debug("looking for outgoing songs ({})...".format(self.name))
        for friend in self.friends:
            for song in friend.incoming:
                if song.friendname == self.name:
                    found = True
                    # TODO: is this the best way to invert ownership?
                    song.friendname = friend.name
                    logging.debug("outoing: {}".format(song))
                    yield song
        if not found:
            logging.debug("no outgoing songs ({})".format(self.name))

    ### methods ##############################################################

    def cleanup(self):
        """Delete all unlinked outgoing songs."""
        logging.info("cleaning up unlinked songs...")
        paths = [os.path.join(self.path_drops, filename)
                 for filename in os.listdir(self.path_drops)]
        for song in self.outgoing:
            try:
                paths.remove(song.source)
            except ValueError:
                pass
        for path in paths:
            logging.info("deleting unlinked: {}".format(path))
            os.remove(path)

    def recommend(self, path, users=None):
        """Recommend a song to a list of users.

        @param path: path to file
        @param users: names of users or None for all

        @return: shared Song
        """
        logging.info("recommending {}...".format(path))
        # TODO: create os-specific symlinks instead of copying the file
        path = shutil.copy(path, self.path_drops)
        song = Song(path)
        for friend in self.friends:
            if not users or friend.name in users:
                song.link(os.path.join(friend.path, self.name))
        return song

    def request(self, song):  # pragma: no cover - not implemented
        """Request a new song."""
        raise NotImplementedError("TODO: implement song requests")

    def check(self):
        """Verify the user's directory is valid."""
        if not os.path.isdir(self.path):
            raise ValueError("not a directory: {}".format(self.path))
        for path in (self.path_private, self.path_drops):
            if not os.path.isdir(path):
                raise ValueError("missing folder: {}".format(path))
        # TODO: also check self.path_library when library support is added
        for path in (self.path_info, self.path_requests, self.path_settings):
            if not os.path.isfile(path):
                raise ValueError("missing file: {}".format(path))

    def delete(self):  # pragma: no cover - not implemented
        """Delete the user."""
        for friend in self.friends:
            path = os.path.join(friend.path, self.name)
            if os.path.exists(path):
                logging.info("deleting {}...".format(path))
                shutil.rmtree(path)
        logging.info("deleting {}...".format(self.path))
        shutil.rmtree(self.path)


def get_info():
    """Return the current computer name and user name."""
    return socket.gethostname(), getpass.getuser()


def get_current(root):
    """Get the current user based on this computer's information.

    @param root: path to root of sharing directory

    @return: current User
    """
    info = get_info()
    logging.debug("looking for {} in {}...".format(info, root))
    for directory in os.listdir(root):
        path = os.path.join(root, directory)
        try:
            user = User(path)
        except ValueError as err:
            logging.debug("invalid user: {}".format(err))
        else:
            if user.info == info:
                logging.info("found user: {}".format(user))
                return user

    raise EnvironmentError("{} not found in {}".format(info, root))
