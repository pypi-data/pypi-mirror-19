"""
#######
Extopen
#######

Provides a cross platform set of tools for opening files externally with the default registered application for
the current operating system.

The currently supported operating systems are Windows NT (eg NT, XP onwards), OSX, Linux.

Please report any bugs/submit patches to: https://github.com/timsavage/extopen/

Usage:

    >>> import extopen
    >>> extopen.is_supported()
    True
    >>> extopen.file("/p/to/my/file")
    >>> extopen.directory("/home/")
    
"""
from __future__ import print_function
import os
import subprocess
import sys


if sys.platform.startswith('darwin'):
    def _execute(p):
        subprocess.call(('open', p))
elif os.name == 'nt':
    def _execute(p):
        os.startfile(p)
elif os.name == 'posix':
    def _execute(p):
        subprocess.call(('xdg-open', p))
else:
    _execute = None


class NotSupported(Exception):
    pass


def is_supported():
    """
    The current OS is a supported by extopen.
    """
    return _execute is not None


def path(p):
    """
    Open a path with the default application.

    :param p: Path to open (file or directory).
    :raises IOError: If the p is not found.
    :raises NotSupported: If extopen is not supported on this OS.

    """
    if _execute is None:
        raise NotSupported("extopen is not supported by the current OS.")
    
    if not os.path.exists(p):
        raise IOError("Path `{}` not found.".format(p))

    return _execute(p)


def file(p):
    """
    Open a file with the default application.

    :param p: Path of the file to open.
    :raises IOError: If file is not found (or is a directory)
    :raises NotSupported: If extopen is not supported on this OS.

    """
    if _execute is None: 
        raise NotSupported("extopen is not supported by the current OS.")

    if not os.path.isfile(p):
        raise IOError("File `{}` not found or is a directory.".format(p))

    return _execute(p)


def directory(p):
    """
    Open a directory with the file browser.

    :param p: Path of the directory to open.
    :raises IOError: If directory is not found (or is a file)
    :raises NotSupported: If extopen is not supported on this OS.

    """
    if _execute is None: 
        raise NotSupported("Open with is not supported on this OS")

    if not os.path.isdir(p):
        raise IOError("Directory `{}` not found of is a file.".format(p))

    return _execute(p)


if __name__ == '__main__':
    if not is_supported():
        print("extopen is not supported by this OS.", file=sys.stderr)
        exit(42)

    if len(sys.argv) != 2:
        print("Usage: {} PATH".format(sys.argv[0]), file=sys.stderr)
        exit(1)

    try:
        path(sys.argv[1])
    except IOError as ex:
        print(str(ex), file=sys.stderr)
        exit(2)

