from typing import Sized, Optional, Iterable


__all__ = (
    'first',
    'last',
)


def first(iterable, or_=None):
    """

    For simple case of a list this is about 3x slower than::

        val = x[0] if len(x) > 0 else or_

    """
    # type: (Iterable[T], T) -> Optional[T]
    return next(iter(iterable), or_)


def last(iterable, or_=None):
    # type: (Sized[T], T) -> Optional[T]
    """Force iterable to be a Sequence on :func:`last` so last cannot be
    called on infinite iterators and generators.

    In the simple list/str case this is about 10x slower than x[-1].
    """
    try:
        return next(iter(reversed(iterable)))
    except StopIteration:
        return or_
