#!/usr/bin/env python

"""
Graphical interface for DropTheBeat.
"""

import tkinter as tk
from tkinter import simpledialog, filedialog

import sys
import argparse
from itertools import chain
import logging

from dtb import GUI, VERSION
from dtb import share, user, song
from dtb import settings


class Application(tk.Frame):  # pylint: disable=R0904,R0924
    """Tkinter application for DropTheBeat."""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # Load the root sharing directory
        self.root = share.find()

        # Load the user
        try:
            self.user = user.get_current(self.root)
        except EnvironmentError:
            msg = "Enter your name in the form 'FirstLast':"
            name = simpledialog.askstring("Create a User", msg).strip(" '")
            self.user = user.User.new(self.root, name)

        # Create variables
        self.path_downloads = tk.StringVar(value=self.user.path_downloads)

        # Initialize the GUI
        self.init(master)
        master.deiconify()

    def init(self, master):  # pylint: disable=R0914
        """Initialize frames and widgets."""

        # Shared settings

        sticky = {'sticky': tk.NSEW}
        pad = {'padx': 5, 'pady': 5}
        stickypad = dict(chain(sticky.items(), pad.items()))

        # Create frames

        frame_settings = tk.Frame(master)
        frame_incoming = tk.Frame(master)
        frame_outgoing = tk.Frame(master)

        frame_div1 = tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN)
        frame_div2 = tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN)

        # Create widets for frames

        label_downloads = tk.Label(frame_settings, text="Downloads:")
        entry_downloads = tk.Entry(frame_settings, state='readonly',
                                   textvariable=self.path_downloads)
        button_downlods = tk.Button(frame_settings, text="...",
                                    command=self.browse_downloads)

        listbox_incoming = tk.Listbox(frame_incoming)
        button_remove = tk.Button(frame_incoming, text="Remove Selected",
                                  command=self.do_remove)
        button_share = tk.Button(frame_incoming, text="Share Songs...",
                                 command=self.do_share)

        listbox_outgoing = tk.Listbox(frame_outgoing)
        button_ignore = tk.Button(frame_outgoing, text="Ignore Selected",
                                  command=self.do_ignore)
        button_download = tk.Button(frame_outgoing, text="Download Songs",
                                    command=self.do_download)

        # Specify frame resizing

        frame_settings.rowconfigure(0, weight=1)
        frame_settings.columnconfigure(0, weight=0)
        frame_settings.columnconfigure(1, weight=1)
        frame_settings.columnconfigure(2, weight=0)

        frame_incoming.rowconfigure(0, weight=1)
        frame_incoming.rowconfigure(1, weight=0)
        frame_incoming.columnconfigure(0, weight=1)
        frame_incoming.columnconfigure(1, weight=1)

        frame_outgoing.rowconfigure(0, weight=1)
        frame_outgoing.rowconfigure(1, weight=0)
        frame_outgoing.columnconfigure(0, weight=1)
        frame_outgoing.columnconfigure(1, weight=1)

        # Pack widgets in frames

        label_downloads.grid(row=0, column=0, **pad)
        entry_downloads.grid(row=0, column=1, **stickypad)
        button_downlods.grid(row=0, column=2, **pad)

        listbox_incoming.grid(row=0, column=0, columnspan=2, **stickypad)
        button_remove.grid(row=1, column=0, sticky=tk.SW, **pad)
        button_share.grid(row=1, column=1, sticky=tk.SE, **pad)

        listbox_outgoing.grid(row=0, column=0, columnspan=2, **stickypad)
        button_ignore.grid(row=1, column=0, sticky=tk.SW, **pad)
        button_download.grid(row=1, column=1, sticky=tk.SE, **pad)

        # Specify master resizing

        master.rowconfigure(0, weight=0)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(4, weight=1)
        master.columnconfigure(0, weight=1)

        # Pack frames in master

        frame_settings.grid(row=0, **stickypad)
        frame_div1.grid(row=1, sticky=tk.EW, padx=10)
        frame_incoming.grid(row=2, **stickypad)
        frame_div2.grid(row=3, sticky=tk.EW, padx=10)
        frame_outgoing.grid(row=4, **stickypad)

    def browse_downloads(self):
        """Browser for a new downloads directory."""
        path = filedialog.askdirectory()
        if path:
            self.user.path_downloads = path
            self.path_downloads.set(self.user.path_downloads)

    def do_remove(self):
        """Remove selected songs."""
        raise NotImplementedError

    def do_share(self):
        """Share songs."""
        raise NotImplementedError

    def do_ignore(self):
        """Ignore selected songs."""
        raise NotImplementedError

    def do_download(self):
        """Download all songs."""
        raise NotImplementedError

    def update(self):
        """Update the list of outgoing and incoming songs."""
        raise NotImplementedError


# TODO: refactor common code
class _HelpFormatter(argparse.HelpFormatter):
    """Command-line help text formatter with wider help text."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, max_help_position=40, **kwargs)


# TODO: refactor common code
class _WarningFormatter(logging.Formatter, object):
    """Logging formatter that always displays a verbose logging
    format for logging level WARNING or higher."""

    def __init__(self, default_format, verbose_format, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_format = default_format
        self.verbose_format = verbose_format

    def format(self, record):
        """Python 3 hack to change the formatting style dynamically."""
        if record.levelno > logging.INFO:
            self._style._fmt = self.verbose_format  # pylint: disable=W0212
        else:
            self._style._fmt = self.default_format  # pylint: disable=W0212
        return super().format(record)


def main(args=None):
    """Process command-line arguments and run the program.
    """
        # Shared options
    debug = argparse.ArgumentParser(add_help=False)
    debug.add_argument('-V', '--version', action='version', version=VERSION)
    debug.add_argument('-v', '--verbose', action='count', default=1,
                       help="enable verbose logging")
    shared = {'formatter_class': _HelpFormatter, 'parents': [debug]}

    # Main parser
    parser = argparse.ArgumentParser(prog=GUI, description=__doc__, **shared)

    # Parse arguments
    args = parser.parse_args(args=args)

    # Configure logging
    _configure_logging(args.verbose)

    # Run the program
    try:
        success = run(args)
    except KeyboardInterrupt:
        logging.debug("program manually closed")
    else:
        if success:
            logging.debug("program exited")
        else:
            logging.debug("program exited with error")
            sys.exit(1)


# TODO: refactor common code
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
    formatter = _WarningFormatter(default_format, verbose_format)
    logging.root.handlers[0].setFormatter(formatter)


def run(args):
    """Start the GUI."""
    root = tk.Tk()
    root.title(GUI)
    root.minsize(500, 500)
    root.withdraw()
    app = Application(master=root)
    return app.mainloop()


if __name__ == '__main__':  # pragma: no cover - manual test
    main()
