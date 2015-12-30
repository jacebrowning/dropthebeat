#!/usr/bin/env python

"""Graphical interface for DropTheBeat."""

import sys
from unittest.mock import Mock
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox, simpledialog, filedialog
except ImportError as err:
    sys.stderr.write("WARNING: {}\n".format(err))
    tk = Mock()
    ttk = Mock()

import os
import argparse
from itertools import chain
import logging

from dtb import GUI, __version__
from dtb import share, user
from dtb.common import SHARED, WarningFormatter
from dtb import settings

_LAUNCH = True


class Application(ttk.Frame):  # pylint: disable=too-many-instance-attributes
    """Tkinter application for DropTheBeat."""

    def __init__(self, master=None, root=None, home=None, name=None):
        ttk.Frame.__init__(self, master)

        # Load the root sharing directory
        self.root = root or share.find(home)

        # Load the user
        self.user = user.User(os.path.join(self.root, name)) if name else None
        try:
            self.user = self.user or user.get_current(self.root)
        except EnvironmentError:

            while True:

                msg = "Enter your name in the form 'First Last':"
                text = simpledialog.askstring("Create a User", msg)
                logging.debug("text: {}".format(repr(text)))
                name = text.strip(" '") if text else None
                if not name:
                    raise KeyboardInterrupt("no user specified")
                try:
                    self.user = user.User.new(self.root, name)
                except EnvironmentError:
                    existing = user.User(os.path.join(self.root, name))
                    msg = "Is this you:"
                    for info in existing.info:
                        msg += "\n\n'{}' on '{}'".format(info[1], info[0])
                    if not existing.info or \
                            messagebox.askyesno("Add to Existing User", msg):
                        self.user = user.User.add(self.root, name)
                        break
                else:
                    break

        # Create variables
        self.path_root = tk.StringVar(value=self.root)
        self.path_downloads = tk.StringVar(value=self.user.path_downloads)
        self.outgoing = []
        self.incoming = []

        # Initialize the GUI
        self.listbox_outgoing = None
        self.listbox_incoming = None
        frame = self.init(master)
        frame.pack(fill=tk.BOTH, expand=1)

        # Show the GUI
        master.deiconify()
        self.update()

    def init(self, root):
        """Initialize frames and widgets."""

        # pylint: disable=line-too-long

        mac = sys.platform == 'darwin'

        # Shared keyword arguments
        kw_f = {'padding': 5}  # constructor arguments for frames
        kw_gp = {'padx': 5, 'pady': 5}  # grid arguments for padded widgets
        kw_gs = {'sticky': tk.NSEW}  # grid arguments for sticky widgets
        kw_gsp = dict(chain(kw_gs.items(), kw_gp.items()))  # grid arguments for sticky padded widgets

        # Configure grid
        frame = ttk.Frame(root, **kw_f)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(4, weight=1)
        frame.columnconfigure(0, weight=1)

        # Create widgets
        def frame_settings(master):
            """Frame for the settings."""
            frame = ttk.Frame(master, **kw_f)

            # Configure grid
            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(1, weight=1)
            frame.columnconfigure(0, weight=0)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=0)

            # Place widgets
            ttk.Label(frame, text="Shared:").grid(row=0, column=0, sticky=tk.W, **kw_gp)
            ttk.Entry(frame, state='readonly', textvariable=self.path_root).grid(row=0, column=1, columnspan=2, **kw_gsp)
            ttk.Label(frame, text="Downloads:").grid(row=1, column=0, sticky=tk.W, **kw_gp)
            ttk.Entry(frame, state='readonly', textvariable=self.path_downloads).grid(row=1, column=1, **kw_gsp)
            ttk.Button(frame, text="...", width=0, command=self.browse_downloads).grid(row=1, column=2, ipadx=5, **kw_gp)

            return frame

        def frame_incoming(master):
            """Frame for incoming songs."""
            frame = ttk.Frame(master, **kw_f)

            # Configure grid
            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(1, weight=0)
            frame.columnconfigure(0, weight=0)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

            # Place widgets
            self.listbox_incoming = tk.Listbox(frame, selectmode=tk.EXTENDED if mac else tk.MULTIPLE)
            self.listbox_incoming.grid(row=0, column=0, columnspan=3, **kw_gsp)
            scroll_incoming = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox_incoming.yview)
            self.listbox_incoming.configure(yscrollcommand=scroll_incoming.set)
            scroll_incoming.grid(row=0, column=2, sticky=(tk.N, tk.E, tk.S))
            ttk.Button(frame, text="\u21BB", width=0, command=self.update).grid(row=1, column=0, sticky=tk.SW, ipadx=5, **kw_gp)
            ttk.Button(frame, text="Ignore Selected", command=self.do_ignore).grid(row=1, column=1, sticky=tk.SW, ipadx=5, **kw_gp)
            ttk.Button(frame, text="Download Selected", command=self.do_download).grid(row=1, column=2, sticky=tk.SE, ipadx=5, **kw_gp)
            return frame

        def frame_outgoing(master):
            """Frame for outgoing songs."""
            frame = ttk.Frame(master, **kw_f)

            # Configure grid
            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(1, weight=0)
            frame.columnconfigure(0, weight=0)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

            # Place widgets
            self.listbox_outgoing = tk.Listbox(frame, selectmode=tk.EXTENDED if mac else tk.MULTIPLE)
            self.listbox_outgoing.grid(row=0, column=0, columnspan=3, **kw_gsp)
            scroll_outgoing = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox_outgoing.yview)
            self.listbox_outgoing.configure(yscrollcommand=scroll_outgoing.set)
            scroll_outgoing.grid(row=0, column=2, sticky=(tk.N, tk.E, tk.S))
            ttk.Button(frame, text="\u21BB", width=0, command=self.update).grid(row=1, column=0, sticky=tk.SW, ipadx=5, **kw_gp)
            ttk.Button(frame, text="Remove Selected", command=self.do_remove).grid(row=1, column=1, sticky=tk.SW, ipadx=5, **kw_gp)
            ttk.Button(frame, text="Share Songs...", command=self.do_share).grid(row=1, column=2, sticky=tk.SE, ipadx=5, **kw_gp)

            return frame

        def separator(master):
            """Widget to separate frames."""
            return ttk.Separator(master)

        # Place widgets
        frame_settings(frame).grid(row=0, **kw_gs)
        separator(frame).grid(row=1, padx=10, pady=5, **kw_gs)
        frame_outgoing(frame).grid(row=2, **kw_gs)
        separator(frame).grid(row=3, padx=10, pady=5, **kw_gs)
        frame_incoming(frame).grid(row=4, **kw_gs)

        return frame

    def browse_downloads(self):
        """Browser for a new downloads directory."""
        path = filedialog.askdirectory()
        logging.debug("path: {}".format(path))
        if path:
            self.user.path_downloads = path
            self.path_downloads.set(self.user.path_downloads)

    def do_remove(self):
        """Remove selected songs."""
        for index in (int(s) for s in self.listbox_outgoing.curselection()):
            self.outgoing[index].ignore()
        self.update()

    def do_share(self):
        """Share songs."""
        paths = filedialog.askopenfilenames()
        if isinstance(paths, str):  # http://bugs.python.org/issue5712
            paths = self.master.tk.splitlist(paths)
        logging.debug("paths: {}".format(paths))
        for path in paths:
            self.user.recommend(path)
        self.update()

    def do_ignore(self):
        """Ignore selected songs."""
        for index in (int(s) for s in self.listbox_incoming.curselection()):
            song = self.incoming[index]
            song.ignore()
        self.update()

    def do_download(self):
        """Download selected songs."""
        indicies = (int(s) for s in self.listbox_incoming.curselection())
        try:
            for index in indicies:
                song = self.incoming[index]
                song.download(catch=False)
        except IOError as exc:
            self.show_error_from_exception(exc, "Download Error")
        self.update()

    def update(self):
        """Update the list of outgoing and incoming songs."""

        # Cleanup outgoing songs
        self.user.cleanup()

        # Update outgoing songs list
        logging.info("updating outgoing songs...")
        self.outgoing = list(self.user.outgoing)
        self.listbox_outgoing.delete(0, tk.END)
        for song in self.outgoing:
            self.listbox_outgoing.insert(tk.END, song.out_string)
        # Update incoming songs list

        logging.info("updating incoming songs...")
        self.incoming = list(self.user.incoming)
        self.listbox_incoming.delete(0, tk.END)
        for song in self.incoming:
            self.listbox_incoming.insert(tk.END, song.in_string)

    @staticmethod
    def show_error_from_exception(exception, title="Error"):
        """Convert an exception to an error dialog."""
        message = str(exception).capitalize().replace(": ", ":\n\n")
        messagebox.showerror(title, message)


def main(args=None):
    """Process command-line arguments and run the program."""

    # Main parser
    parser = argparse.ArgumentParser(prog=GUI, description=__doc__, **SHARED)
    parser.add_argument('--home', metavar='PATH', help="path to home directory")
    # Hidden argument to override the root sharing directory path
    parser.add_argument('--root', metavar="PATH", help=argparse.SUPPRESS)
    # Hidden argument to run the program as a different user
    parser.add_argument('--test', metavar='"First Last"',
                        help=argparse.SUPPRESS)

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


def _configure_logging(verbosity=0):
    """Configure logging using the provided verbosity level (0+)."""

    # Configure the logging level and format
    if verbosity == 0:
        level = settings.VERBOSE_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.VERBOSE_LOGGING_FORMAT
    else:
        level = settings.VERBOSE2_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE_LOGGING_FORMAT

    # Set a custom formatter
    logging.basicConfig(level=level)
    formatter = WarningFormatter(default_format, verbose_format)
    logging.root.handlers[0].setFormatter(formatter)


def run(args):
    """Start the GUI."""

    # Exit if tkinter is not available
    if isinstance(tk, Mock) or isinstance(ttk, Mock):
        logging.error("tkinter is not available")
        return False

    else:

        root = tk.Tk()
        root.title("{} (v{})".format(GUI, __version__))
        root.minsize(500, 500)

        # Map the Mac 'command' key to 'control'
        if sys.platform == 'darwin':
            root.bind_class('Listbox', '<Command-Button-1>',
                            root.bind_class('Listbox', '<Control-Button-1>'))

        # Temporarily hide the window for other dialogs
        root.withdraw()

        # Start the application
        app = Application(master=root, home=args.home,
                          root=args.root, name=args.test)
        if _LAUNCH:
            app.mainloop()

        return True


if __name__ == '__main__':  # pragma: no cover (manual test)
    main()
