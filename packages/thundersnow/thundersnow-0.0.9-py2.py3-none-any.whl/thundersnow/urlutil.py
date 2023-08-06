try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

import posixpath


__all__ = (
    'join',
)


def join(base, path):
    # type: (str, str) -> str
    """
    >>> urlutil.join('a/b', 'c/d')
    'a/b/c/d'
    >>> urlutil.join('/a/b/', 'c/d')
    '/a/b/c/d'
    >>> urlutil.join('https://example.com/a', 'b/c/d')
    'https://example.com/a/b/c/d'
    >>> urlutil.join('https://example.com/a/', 'b/c/d')
    'https://example.com/a/b/c/d'
    >>> urlutil.join('https://example.com/a/', '/b/c/d')
    'https://example.com/a/b/c/d'
    """
    scheme, netloc, basepath, params, query, fragment = urlparse(base)
    newpath = posixpath.join(basepath, path)
    parts = (scheme, netloc, newpath, params, query, fragment)
    return urlunparse(parts)
