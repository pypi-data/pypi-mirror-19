from collections import namedtuple, OrderedDict

from typing import Any, NamedTuple

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

import six
from six import iteritems, iterkeys
import boltons.typeutils


__all__ = (
    'immutable',
    'sentinel',
    'Namespace'
)


def immutable(clazz_name, **attrs):
    # type: (str, **Any) -> NamedTuple
    """Immutable object factory backed by a namedtuple. It is only truly
    immutable if the attributes are immutable as well. Since the
    backing data type is a namedtuple, the returned object has a lot of
    free functionality.

    Assume:

    >>> Color = immutable('Color', blue=1, red=2, green=3, yellow=4)

    - Dot access attributes: `Color.blue`
    - A sane default __str__ and __repr__ implementation::

    >>> print(Color)
    Color(blue=1, green=3, yellow=4, red=2)

    - Iterable and indexable::

    >>> for color in Color: print(color)
    1
    3
    4
    2

    - Immutable attributes::

    >>> Color.blue = 'blue'
    AttributeError: can't set attribute

    - Automatic shallow dict conversion (not recursive)::

    >>> print(Color._asdict())
    OrderedDict([('blue', 1), ('green', 3), ('yellow', 4), ('red', 2)])

    :param clazz_name: The name given to the namedtuple, this is
        useful for str(obj) and debugging. Giving a name to the
        immutable object makes it clear what it is. Otherwise it is
        just a super tuple.

    :param attrs: The attributes of the immutable object
    """
    ImmutableClass = namedtuple(clazz_name, attrs.keys())
    return ImmutableClass(**attrs)


def sentinel(name):
    # type: (str) -> Any
    """Returns a named sentinel object.

    Often used for _missing implementations or implementation specific
    nulls. It is important to give these sentinels
    UPPER_SNAKE_CASE_NAMES with a low chance of name collisions so if
    they are logged for some reason, it stands out.

    >>> data = dict(value=None)
    >>> _Missing = sentinel('MISSING')
    >>> print(data.get('value', _Missing) is _Missing)
    False
    >>> print(data.get('value', _Missing) is None)
    True
    >>> print(_Missing)
    MISSING
    """
    name = name.upper()
    return boltons.typeutils.make_sentinel(var_name=name)


if six.PY3:
    from types import SimpleNamespace

    class Namespace(SimpleNamespace, Mapping):

        def __getitem__(self, name):
            return getattr(self, name)

        def __setitem__(self, name, value):
            setattr(self, name, value)

        def __len__(self):
            return len(self.__dict__)

        def __iter__(self):
            return iterkeys(self.__dict__)

        def __copy__(self):
            new = {}
            for name, value in iteritems(self.__dict__):
                if isinstance(value, list):
                    new[name] = value[:]
                elif isinstance(value, Mapping):
                    new[name] = value.copy()
                else:
                    new[name] = value
            return type(self)(**new)

else:
    class Namespace(Mapping):
        """Dynamic dot access attribute object"""
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        def __repr__(self):
            keys = sorted(k for k in self.__dict__ if not k.startswith('_'))
            items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
            return "{}({})".format(type(self).__name__, ", ".join(items))

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __getitem__(self, name):
            return getattr(self, name)

        def __setitem__(self, name, value):
            setattr(self, name, value)

        def __len__(self):
            return len(self.__dict__)

        def __iter__(self):
            return iterkeys(self.__dict__)

        def __copy__(self):
            new = {}
            for name, value in iteritems(self.__dict__):
                if isinstance(value, list):
                    new[name] = value[:]
                elif isinstance(value, Mapping):
                    new[name] = value.copy()
                else:
                    new[name] = value
            return type(self)(**new)
