#!/usr/bin/env python

"""
Classes and functions to interact with sharing services.
"""

import os
import getpass
import logging

SHARE = 'DropTheBeat'
SERVICES = ('Dropbox',)

ROOTS = (
    r"C:\Users",
    r"C:\Documents and Settings",
    r"/home",
    r"/Users",
)


def find(top=None):
    """Return the path to a sharing location."""

    top = top or _default_top()

    logging.debug("looking for '{}' in {}...".format(SHARE, top))
    for directory in os.listdir(top):
        if directory in SERVICES:
            service = os.path.join(top, directory)
            for dirpath, _, _, in os.walk(service):
                path = os.path.join(dirpath, SHARE)
                if os.path.isdir(path):
                    logging.info("found share: {}".format(path))
                    return path

    raise EnvironmentError("no '{}' directory found".format(SHARE))


def _default_top():
    """Return the default search path."""

    username = getpass.getuser()
    for root in ROOTS:
        path = os.path.join(root, username)
        if os.path.isdir(path):  # pragma: no cover - manual test
            return path

    raise EnvironmentError("no home found for '{}'".format(username))
