#!/usr/bin/env python

"""
Classes and functions to interact with songs.
"""

import os
import shutil
import hashlib
import logging

import yaml


class Song(object):
    """Represents a song file or link."""

    def __init__(self, path, downloads=None, friendname=None):
        self.path = path
        self.downloads = downloads
        self.friendname = friendname

    def __str__(self):
        return str(self.path)  # TODO: add link following

    def link(self, dirpath):
        """Create a link to the song in the specified directory."""
        relpath = os.path.relpath(self.path, dirpath)
        md5 = hashlib.md5()
        md5.update(relpath.encode('utf-8'))
        filename = "{}.yml".format(md5.hexdigest())
        path = os.path.join(dirpath, filename)
        logging.info("creating link {}...".format(path))
        with open(path, 'w') as link:
            data = {'link': relpath}
            link.write(yaml.dump(data, default_flow_style=False))

    def download(self):
        """Move the song to the user's downlod directory."""
        assert self.downloads  # TODO: add a better error
        src = self.path
        # Determine if the song file is actually a link
        if self.path.endswith('.yml'):
            with open(self.path, 'r') as yml:
                text = yml.read()
                data = yaml.load(text)  # TODO: handle parser errors
                if data:
                    relpath = data.get('link', None)
                    if relpath:
                        dirpath = os.path.dirname(self.path)
                        path = os.path.join(dirpath, relpath)
                        src = os.path.normpath(path)
                    else:
                        logging.debug("non-link YAML: {}".format(self.path))
        # Move the file or copy from the link
        try:
            if src == self.path:
                logging.info("moving {}...".format(src, self.downloads))
                # Copy then delete in case the opperation is cancelled
                shutil.copy(src, self.downloads)
                os.remove(src)
            else:
                if os.path.exists(src):
                    logging.info("copying {}...".format(src, self.downloads))
                    shutil.copy(src, self.downloads)
                    os.remove(self.path)
                else:
                    logging.debug("unknown link target: {}".format(src))
                    logging.warning("broken link: {}".format(self.path))
                    os.remove(self.path)
        except IOError as error:
            logging.warning(error)

    def ignore(self):
        """Delete the song."""
        logging.info("deleting {}...".format(self.path))
        os.remove(self.path)
