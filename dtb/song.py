#!/usr/bin/env python

"""
Classes and functions to interact with songs.
"""

import os
import shutil
import hashlib
import base64
import logging

import yaml


class Song(object):
    """Represents a song file or link."""

    def __init__(self, path, downloads=None, friendname=None):
        self.path = path
        self.downloads = downloads
        self.friendname = friendname

    def __str__(self):
        return str(self.path)

    def link(self, dirpath):
        """Create a link to the song in the specified directory."""
        if not os.path.isdir(dirpath):
            logging.warning("creating missing folder: {}".format(dirpath))
            os.makedirs(dirpath)
        relpath = os.path.relpath(self.path, dirpath)
        md5 = hashlib.md5()
        md5.update(relpath.encode('utf-8'))
        base = base64.urlsafe_b64encode(md5.digest()).decode('utf-8')
        filename = "{}.yml".format(base)
        path = os.path.join(dirpath, filename)
        logging.info("creating link {}...".format(path))
        with open(path, 'w') as link:
            data = {'link': relpath}
            link.write(yaml.dump(data, default_flow_style=False))

    @property
    def source(self):
        """If the song is a link, return its source. Otherwise its path."""
        src = self.path
        if self.path.endswith('.yml'):
            with open(self.path, 'r') as yml:
                text = yml.read()
                try:
                    data = yaml.load(text)
                except yaml.parser.ParserError:  # pylint: disable=E1101
                    logging.warning("invalid YAML: {}".format(self.path))
                    data = None
                if data:
                    relpath = data.get('link', None)
                    if relpath:
                        dirpath = os.path.dirname(self.path)
                        path = os.path.join(dirpath, relpath)
                        src = os.path.normpath(path)
                    else:
                        logging.debug("non-link YAML: {}".format(self.path))
        return src

    @property
    def in_string(self):
        """Get the string representation for an incoming song."""
        filename = os.path.basename(self.source)
        return "{} (from {})".format(filename, self.friendname)

    @property
    def out_string(self):
        """Get the string representation for an incoming song."""
        filename = os.path.basename(self.source)
        return "{} (to {})".format(filename, self.friendname)

    def download(self):
        """Move the song to the user's downlod directory.

        @return: path to downloaded file or None on broken links
        """
        assert self.downloads  # only called in cases where downloads is set
        # Determine if the song file is actually a link
        src = self.source
        dst = None
        # Move the file or copy from the link
        try:
            if src == self.path:
                logging.info("moving {}...".format(src, self.downloads))
                # Copy then delete in case the opperation is cancelled
                dst = shutil.copy(src, self.downloads)
                os.remove(src)
            else:
                if os.path.exists(src):
                    logging.info("copying {}...".format(src, self.downloads))
                    dst = shutil.copy(src, self.downloads)
                    os.remove(self.path)
                else:
                    logging.debug("unknown link target: {}".format(src))
                    logging.warning("broken link: {}".format(self.path))
                    os.remove(self.path)
        except IOError as error:
            # TODO: these errors need to be left uncaught for the GUI
            logging.warning(error)
        return dst

    def ignore(self):
        """Delete the song."""
        logging.info("deleting {}...".format(self.path))
        os.remove(self.path)
