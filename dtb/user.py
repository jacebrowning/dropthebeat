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
    INFO = os.path.join(PRIVATE, 'info.yml')  # list of computer settings
    SETTINGS = os.path.join(PRIVATE, 'settings.yml')  # general preferences
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
        @param root: path to root of sharing directory
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
        info = get_info()
        data = [{'computer': info[0],
                 'username': info[1],
                 'downloads': downloads}]
        text = yaml.dump(data, default_flow_style=False)
        logging.debug("saving {}...".format(user.path_info))
        with open(user.path_info, 'w') as outfile:
            outfile.write(text)
        # Create settings
        data = {}
        text = yaml.dump(data, default_flow_style=False)
        logging.debug("saving {}...".format(user.path_settings))
        with open(user.path_settings, 'w') as outfile:
            outfile.write(text)
        # Create requests
        data = []
        text = yaml.dump(data, default_flow_style=False)
        logging.debug("saving {}...".format(user.path_requests))
        with open(user.path_requests, 'w') as outfile:
            outfile.write(text)
        # Create folders for friends
        for name in os.listdir(root):
            friendpath = os.path.join(root, name)
            if name != user.name and os.path.isdir(friendpath):
                User._makedir(os.path.join(user.path, name))
                User._makedir(os.path.join(friendpath, user.name))
        # Return the new user
        logging.info("created user: {}".format(user))
        user.check()
        return user

    @staticmethod
    def add(root, name, downloads=None):
        """Add the current computer's information to an existing user.
        @param root: path to root of sharing directory
        @param name: name of existing user's sharing folder
        @param downloads: path to user's downloads directory

        @return: existing User
        """
        logging.debug("adding to user '{}'...".format(name))
        downloads = downloads or os.path.expanduser('~/Downloads')
        # Get the existing user
        user = User(os.path.join(root, name))
        # Update info
        logging.debug("loading {}...".format(user.path_info))
        with open(user.path_info, 'r') as infile:
            text = infile.read()
        data = yaml.load(text)
        info = get_info()
        if not isinstance(data, list):
            logging.warning("data reset due to config format change")
            data = []
        data.append({'computer': info[0],
                     'username': info[1],
                     'downloads': downloads})
        text = yaml.dump(data, default_flow_style=False)
        logging.debug("saving {}...".format(user.path_info))
        with open(user.path_info, 'w') as outfile:
            outfile.write(text)
        # Return the updated user
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
        """Get a list of the user's information."""
        infos = []
        logging.debug("loading {}...".format(self.path_info))
        with open(self.path_info, 'r') as infile:
            text = infile.read()
        data = yaml.load(text)
        if isinstance(data, list):
            for info in data:
                computer = info.get('computer', None)
                username = info.get('username', None)
                infos.append((computer, username))
        return infos

    @property
    def path_downloads(self):
        """Get the user's download path."""
        downloads = None
        info = get_info()
        logging.debug("loading {}...".format(self.path_info))
        with open(self.path_info, 'r') as infile:
            text = infile.read()
        data = yaml.load(text)
        if isinstance(data, list):
            for info2 in data:
                comp_user = info[:2]
                comp_user2 = (info2.get('computer', None),
                              info2.get('username', None))
                if comp_user == comp_user2:
                    downloads = info2.get('downloads', None)
                    break
        return downloads

    @path_downloads.setter
    def path_downloads(self, downloads):
        """Set the user's download path."""
        # TODO: refactor all into one common reader and writer
        info = get_info()
        logging.debug("loading {}...".format(self.path_info))
        with open(self.path_info, 'r') as infile:
            text = infile.read()
        data = yaml.load(text)
        if not isinstance(data, list):
            logging.warning("data reset due to config format change")
            data = []
        for index, info2 in enumerate(data):
            if (info[0] == info2.get('computer', None) and
                info[1] == info2.get('username', None)):
                info2['downloads'] = downloads
                data[index] = info2
                break
        else:
            data.append({'computer': info[0],
                         'username': info[1],
                         'downloads': downloads})
        text = yaml.dump(data, default_flow_style=False)
        logging.debug("saving {}...".format(self.path_info))
        with open(self.path_info, 'w') as outfile:
            outfile.write(text)

    @property
    def friends(self):
        """Iterate through the user's friends."""
        for friend in self._iter_friends():
            yield friend

    def _iter_friends(self, clean=False):
        """Iterate through the user's friends with optional cleanup."""
        for directory in os.listdir(self.root):
            path = os.path.join(self.root, directory)
            try:
                user = User(path)
            except ValueError as err:
                logging.debug("invalid user: {}".format(err))
                if clean and os.path.isdir(path):
                    logging.warning("deleting invalid user: {}".format(path))
                    self._delete(path)
            else:
                if user.name != self.name:
                    yield user

    @property
    def incoming(self):
        """Iterate through the list of incoming songs."""
        found = False
        logging.debug("looking for incoming songs ({})...".format(self.name))
        for friendname in os.listdir(self.path):
            friendpath = os.path.join(self.path, friendname)
            if friendname != User.PRIVATE and os.path.isdir(friendpath):
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
                    logging.debug("outgoing: {}".format(song))
                    yield song
        if not found:
            logging.debug("no outgoing songs ({})".format(self.name))

    ### methods ##############################################################

    def cleanup(self):
        """Delete invalid users, unlinked songs, and empty directories."""
        logging.info("cleaning up {}...".format(self.root))
        # Delete unliked songs
        paths = [os.path.join(self.path_drops, name)
                 for name in os.listdir(self.path_drops)]
        for song in self.outgoing:
            try:
                paths.remove(song.source)
            except ValueError:
                pass
        for path in paths:
            logging.info("deleting unlinked: {}".format(path))
            self._delete(path)
        # Delete non-friend directories
        names = [friend.name for friend in self._iter_friends(clean=True)]
        for name in os.listdir(self.path):
            path = os.path.join(self.path, name)
            if name not in names and name != User.PRIVATE:
                logging.warning("deleting non-friend: {}".format(path))
                self._delete(path)

    @staticmethod
    def _makedir(path):
        """Create a directory if needed."""
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def _delete(path):
        """Delete a file or directory."""
        logging.debug("deleting {}...".format(path))
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def recommend(self, path, users=None):
        """Recommend a song to a list of users.

        @param path: path to file
        @param users: names of users or None for all

        @return: shared Song
        """
        logging.info("recommending {}...".format(path))
        shutil.copy(path, self.path_drops)
        song = Song(os.path.join(self.path_drops, os.path.basename(path)))
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
            if info in user.info:
                logging.info("found user: {}".format(user))
                return user

    raise EnvironmentError("{} not found in {}".format(info, root))
