"""Package for DropTheBeat."""

__project__ = 'DropTheBeat'
__version__ = '0.1'

CLI = 'dtb'
GUI = __project__
VERSION = __project__ + '-' + __version__

PYTHON_VERSION = 3, 3

import sys
if not sys.version_info >= PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))
