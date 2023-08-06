from typing import Union, Optional, TypeVar


__all__ = (
    'maybe',
    'given'
)


T = TypeVar('T')
S = TypeVar('S')


class maybe(object):
    """
     Shorthand for the ugly python ternary::

        val = obj if obj is not None else other

    val = maybe(object).else_(other)
    """

    def __init__(self, value):
        # type: (Optional[T]) -> None
        self._value = value

    def else_(self, other):
        # type: (S) -> Union[T, S]
        if self._value is None:
            return other
        return self._value


class given(maybe):
    """
    given(obj).may_have('hello').else_(str)
    """
    def may_have(self, name):
        # type: (str) -> maybe
        return maybe(getattr(self._value, name, None))
