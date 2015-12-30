"""Classes and functions to interact with sharing services."""

import os
import logging


SERVICES = (
    'Dropbox',
    'Dropbox (Personal)',
)
SHARE = 'DropTheBeat'
SHARE_DEPTH = 3  # number of levels to search for share directory


def find(home=None):
    """Return the path to a sharing location."""

    home = home or os.path.expanduser("~")

    logging.debug("looking for service in {}...".format(home))
    for directory in os.listdir(home):
        if directory in SERVICES:
            service = os.path.join(home, directory)
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
