#!/usr/bin/env python

"""Command-line interface for DropTheBeat."""

import os
import sys
import time
import argparse
import logging

from dtb import CLI
from dtb import share, user, gui
from dtb.common import SHARED, WarningFormatter
from dtb import settings


def main(args=None):
    """Process command-line arguments and run the program."""

    # Main parser
    parser = argparse.ArgumentParser(prog=CLI, description=__doc__, **SHARED)
    parser.add_argument('-g', '--gui', action='store_true',
                        help="launch the GUI")
    parser.add_argument('-d', '--daemon', action='store_true',
                        help="if terminal mode, run forever")
    parser.add_argument('-q', '--no-log', action='store_true',
                        help="do not create a log for downloads")
    # TODO: support sharing multiple songs
    parser.add_argument('-s', '--share', metavar='PATH',
                        help="recommend a song")
    parser.add_argument('-i', '--incoming', action='store_true',
                        help="display the incoming songs")
    parser.add_argument('-o', '--outgoing', action='store_true',
                        help="display the outgoing songs")
    parser.add_argument('-u', '--users', metavar='n', nargs='*',
                        help="filter to the specified usernames")
    parser.add_argument('-n', '--new', metavar='"First Last"',
                        help="create a new user")
    parser.add_argument('-x', '--delete', action='store_true',
                        help="delete the current user")
    # Hidden argument to override the root sharing directory path
    parser.add_argument('--root', metavar="PATH", help=argparse.SUPPRESS)
    # Hidden argument to override the home directory
    parser.add_argument('--home', metavar='PATH', help=argparse.SUPPRESS)
    # Hidden argument to run the program as a different user
    parser.add_argument('--test', metavar='"First Last"',
                        help=argparse.SUPPRESS)

    # Parse arguments
    args = parser.parse_args(args=args)

    # Configure logging
    _configure_logging(args.verbose)

    # Run the program
    try:
        success = _run(args, os.getcwd(), parser.error)
    except KeyboardInterrupt:
        logging.debug("command canceled")
    else:
        if success:
            logging.debug("command succeeded")
        else:
            logging.debug("command failed")
            sys.exit(1)


def _configure_logging(verbosity=0):
    """Configure logging using the provided verbosity level (0+)."""

    # Configure the logging level and format
    if verbosity == 0:
        level = settings.DEFAULT_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.VERBOSE_LOGGING_FORMAT
    elif verbosity == 1:
        level = settings.VERBOSE_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE_LOGGING_FORMAT
    elif verbosity == 2:
        level = settings.VERBOSE2_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE_LOGGING_FORMAT
    else:
        level = settings.VERBOSE2_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE2_LOGGING_FORMAT

    # Set a custom formatter
    logging.basicConfig(level=level)
    formatter = WarningFormatter(default_format, verbose_format)
    logging.root.handlers[0].setFormatter(formatter)


def _run(args, cwd, err):  # pylint: disable=W0613
    """Process arguments and run the main program.

    @param args: Namespace of CLI arguments
    @param cwd: current working directory
    @param err: function to call for CLI errors
    """
    # Run the GUI
    if args.gui:
        logging.info("launching the GUI...")
        return gui.run(args)

    # Find the sharing directory
    root = args.root or share.find()

    # Create a new user and exit
    if args.new:
        return _new(args.new, root)

    # Get the current user
    if args.test:
        this = user.User(os.path.join(root, args.test))
    else:
        this = user.get_current(root)
    this.cleanup()

    # Delete user and exit
    if args.delete:
        this.delete()
        print("deleted: {}".format(this))
        return True

    # Display incoming, share a song, and/or display outgoing and exit
    if any((args.incoming, args.share, args.outgoing)):

        if args.incoming:
            logging.info("displaying incoming songs...")
            for song in this.incoming:
                print("incoming: {}".format(song))

        if args.share:
            path = os.path.abspath(args.share)
            song = this.recommend(path, args.users)
            print("shared: {}".format(path))

        if args.outgoing:
            logging.info("displaying outgoing songs...")
            for song in this.outgoing:
                print("outgoing: {}".format(song))

        return True

    # Run the command-line interface loop
    logging.info("starting the main loop...")
    return _loop(this, args.daemon, not args.no_log)


def _new(name, root):
    """Create a new user."""
    try:
        this = user.User.new(root, name)
        print("created: {}".format(this))
    except EnvironmentError as error:
        logging.error(error)
        return False

    return True


def _loop(this, daemon, log):
    """Run the main CLI loop."""
    while True:
        for song in this.incoming:
            path = song.download()
            if path:
                print("downloaded: {}".format(path))
                # Append download message to the log
                if log:
                    dirpath, filename = os.path.split(path)
                    logpath = os.path.join(dirpath, CLI + '.log')
                    with open(logpath, 'a') as log:
                        msg = "{} from {}".format(filename, song.friendname)
                        log.write(msg + '\n')
        if daemon:
            logging.debug("daemon sleeping for 5 seconds...")
            time.sleep(5)
        else:
            break

    return True


if __name__ == '__main__':  # pragma: no cover (manual test)
    main()
