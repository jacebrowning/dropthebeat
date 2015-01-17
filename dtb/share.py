"""Classes and functions to interact with sharing services."""

import os
import getpass
import logging

ROOTS = (
    r"C:\Users",
    r"/Users",
    r"/home",
)
SERVICES = (
    'Dropbox',
    'Dropbox (Personal)',
)
SHARE = 'DropTheBeat'
SHARE_DEPTH = 3  # number of levels to search for share directory


def find(top=None):
    """Return the path to a sharing location."""

    top = top or _default_top()

    logging.debug("looking for service in {}...".format(top))
    for directory in os.listdir(top):
        if directory in SERVICES:
            service = os.path.join(top, directory)
            logging.debug("found service: {}".format(service))
            logging.debug("looking for '{}' in {}...".format(SHARE, service))
            for dirpath, dirnames, _, in os.walk(service):
                depth = dirpath.count(os.path.sep) - service.count(os.path.sep)
                if depth >= SHARE_DEPTH:
                    del dirnames[:]
                    continue
                path = os.path.join(dirpath, SHARE)
                if os.path.isdir(path) and \
                        not os.path.isfile(os.path.join(path, 'setup.py')):
                    logging.info("found share: {}".format(path))
                    return path

    raise EnvironmentError("no '{}' folder found".format(SHARE))


def _default_top():
    """Return the default search path."""

    username = getpass.getuser()
    logging.debug("looking for home...")
    for root in ROOTS:
        path = os.path.join(root, username)
        if os.path.isdir(path):  # pragma: no cover - manual test
            logging.debug("found home: {}".format(path))
            return path

    raise EnvironmentError("no home found for '{}'".format(username))
