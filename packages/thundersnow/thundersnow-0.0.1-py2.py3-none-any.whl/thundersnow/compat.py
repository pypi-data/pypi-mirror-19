import six


__all__ = (
    'scandir',
    'PurePath',
    'Path'
    'StringIO',
    'EMPTY_UTF8_STRING',
    'Dirent'
)


if six.PY3:
    from os import scandir, Dirent
    from pathlib import Path, PurePath
    from ioutil import StringIO
    EMPTY_UTF8_STRING = str()
else:
    from scandir import scandir, Dirent
    from pathlib2 import Path, PurePath
    from StringIO import StringIO
    EMPTY_UTF8_STRING = unicode()