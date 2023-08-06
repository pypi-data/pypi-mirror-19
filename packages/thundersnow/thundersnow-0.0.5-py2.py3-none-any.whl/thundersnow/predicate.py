from typing import Any, Sized, Callable
import six


__all__ = (
    'is_none',
    'is_not_none',
    'is_empty',
    'is_not_empty',
    'is_blank',
    'is_not_blank',
    'not_'
)


def is_none(obj):
    # type: (Any) -> bool
    return obj is None


def is_not_none(obj):
    # type: (Any) -> bool
    return obj is not None


def is_empty(sequence):
    # type: (Sized) -> bool
    return len(sequence) == 0


def is_not_empty(sequence):
    # type: (Sized) -> bool
    return len(sequence) != 0


def is_blank(obj):
    # type: (Sized) -> bool
    if isinstance(obj, six.string_types):
        return is_empty(obj.strip())

    return is_none(obj) or is_empty(obj)


def is_not_blank(obj):
    if isinstance(obj, six.string_types):
        return is_not_empty(obj.strip())

    return is_not_none(obj) and is_not_empty(obj)


def always_true(obj):
    # type: (Any) -> bool
    return True


def always_false(obj):
    # type: (Any) -> bool
    return False


def not_(predicate):
    # type: (Callable[[Any], bool]) -> bool
    @six.wraps(predicate)
    def complement(arg):
        return not predicate(arg)

    return complement
