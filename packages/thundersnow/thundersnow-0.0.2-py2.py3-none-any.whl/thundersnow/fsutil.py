from typing import Union, Generator, Optional
from fnmatch import fnmatch

from thundersnow.compat import scandir, DirEntry
from thundersnow.compat import Path, PurePath
from toolz.compatibility import filter
from toolz import flip, compose, juxt, identity

from enum import Enum


__all__ = (
    'ls',
    'find',
    'FileType'
)


class FileType(Enum):
    file = 'f'
    directory = 'd'
    link = 'l'
    any = None


def _ls_internal(directory, max_depth, current_depth):
    # type: (Union[str, Path], Optional[int], int) -> Generator[Dirent, None, None]
    if (max_depth is not None) and (current_depth > max_depth):
        return
    for entry in scandir(str(directory)):
        yield entry
        if entry.is_dir():
            for file in _ls_internal(entry.path, max_depth, current_depth + 1):
                yield file


def ls(directory, recursive=False):
    # type: (Union[str, PurePath], bool) -> Generator[Path, None, None]
    max_depth = None if recursive else 1
    return (Path(e.path) for e in _ls_internal(directory, max_depth, 1))


def _find_internal(directory, key=identity):
    # type: (Union[str, PurePath], bool) -> Generator[Path, None, None]
    paths = ls(directory, recursive=True)

    if key is None:
        return paths

    return filter(key, paths)


def is_file_type(path, ftype):
    # type: (PurePath, Optional[FileType]) -> bool
    if not isinstance(ftype, FileType):
        ftype = FileType(ftype)
    if not isinstance(path, PurePath):
        path = Path(path)

    if ftype == FileType.any:
        return True
    elif ftype == FileType.file:
        return path.is_file()
    elif ftype == FileType.directory:
        return path.is_dir()
    elif ftype == FileType.link:
        return path.is_symlink()

    return False


def find(directory, name='*', ftype=FileType.any):
    # type: (Union[str, PurePath], str, FileType) -> Generator[Path, None, None]
    validators = juxt(
        compose(flip(fnmatch, name), str),  # Convert the Path object to string and match str against name
        flip(is_file_type, ftype))          # Check if the Path object is of FileType
    key = compose(all, validators)

    return _find_internal(directory, key=key)
