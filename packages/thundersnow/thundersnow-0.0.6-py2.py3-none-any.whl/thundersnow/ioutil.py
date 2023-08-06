import contextlib
import sys

from thundersnow.compat import StringIO, PurePath, Path
from thundersnow.compat import EMPTY_UTF8_STRING


__all__ = (
    'iterlines',
    'fulltext',
    'capture_print'
)


def iterlines(path):
    if not isinstance(path, PurePath):
        path = Path(path)

    with path.open('r', encoding='utf-8', errors='backslashreplace') as infile:
        for line in infile:
            yield line


def fulltext(path):
    return EMPTY_UTF8_STRING.join(iterlines(path))


@contextlib.contextmanager
def capture_print():
    out, err = StringIO(), StringIO()
    stdout, stderr = sys.stdout, sys.stderr

    try:
        sys.stdout, sys.stderr = out, err
        yield out, err
    finally:
        sys.stdout, sys.stderr = stdout, stderr


