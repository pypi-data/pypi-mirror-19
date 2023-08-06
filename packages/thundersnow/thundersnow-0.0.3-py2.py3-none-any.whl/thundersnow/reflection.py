# -*- coding: utf-8 -*-
from __future__ import absolute_import

import __builtin__
import inspect
import types

from typing import Any


__all__ = (
    'module_path',
    'module_name',
    'class_name',
    'class_path',
    'name_of',
    'is_builtin_type',
)


_builtin_types = {t for name, t in inspect.getmembers(__builtin__, inspect.isclass)}
_builtin_types.update({t for name, t in inspect.getmembers(types, inspect.isclass)})
_missing = object()


def module_path(obj):
    # type: (Any) -> str
    """Return the module path of any object"""
    if inspect.ismodule(obj):
        return obj.__name__

    module = inspect.getmodule(obj)
    name = getattr(module, '__name__', _missing)

    if name is _missing:
        return module_path(type(obj))

    return str(name)


def module_name(obj):
    # type: (Any) -> str
    """Return the module name of any object."""
    # some.path.to.module -> [some, path, to, module]
    parts = module_path(obj).rsplit('.', 1)
    return parts[-1]


def class_name(obj):
    # type: (Any) -> str
    """Return the class name of any object."""
    if inspect.isclass(obj):
        return obj.__name__
    else:
        return obj.__class__.__name__


def class_path(obj):
    # type: (Any) -> str
    """Return the fully qualified import path of an objects type"""
    if inspect.ismodule(obj):
        return module_path(obj)
    return '.'.join((module_path(obj), class_name(obj)))


def name_of(obj):
    # type: (Any) -> str
    name = getattr(obj, '__name__', _missing)
    if name is not _missing:
        return str(name)
    elif inspect.ismodule(obj):
        return module_name(obj)

    return class_name(obj)


def is_builtin_type(obj):
    # type: (Any) -> bool
    return obj in _builtin_types
