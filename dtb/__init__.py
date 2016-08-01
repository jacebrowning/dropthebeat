"""Package for DropTheBeat."""

import sys

__project__ = 'DropTheBeat'
__version__ = '1.0'

CLI = 'dtb'
GUI = __project__
VERSION = "{0} v{1}".format(__project__, __version__)

PYTHON_VERSION = 3, 3

if sys.version_info < PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
