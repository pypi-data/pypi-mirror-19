import six


__all__ = (
    'scandir',
    'PurePath',
    'Path'
    'StringIO',
    'EMPTY_UTF8_STRING',
    'DirEntry'
)


if six.PY3:
    from os import scandir, DirEntry
    from pathlib import Path, PurePath
    from io import StringIO
    EMPTY_UTF8_STRING = str()
else:
    from scandir import scandir
    from scandir import Dirent as DirEntry
    from pathlib2 import Path, PurePath
    from StringIO import StringIO
    EMPTY_UTF8_STRING = unicode()