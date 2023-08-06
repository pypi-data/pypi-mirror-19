# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from errno import EEXIST
from logging import getLogger
from os import access, chmod, getpid, listdir, lstat, makedirs, rename, unlink, walk
from os.path import abspath, basename, dirname, isdir, isfile, islink, join, lexists
from stat import S_IEXEC, S_IMODE, S_ISDIR, S_ISLNK, S_ISREG, S_IWRITE
from uuid import uuid4
import sys

__all__ = ["rm_rf"]

log = getLogger(__name__)

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str
else:
    text_type = unicode


def rm_rf(path, max_retries=5, trash=True):
    """
    Completely delete path

    Parameters
    ----------
    path : str
        Path to file or directory.
    max_retries : int, optional
        Number of times to retry on failure.

        The default is 5. This only applies to deleting a directory.
    trash : bool, optional
        If ``True`` and removing path fails, move files to the trash directory.

    Returns
    -------
    bool
        ``True`` if file/directory was removed successfully, otherwise
        ``False``.
    """
    try:
        path = abspath(path)
        log.debug("rm_rf %s", path)
        if isdir(path):
            # On Windows, always move to trash first.
            if trash and on_win:
                move_result = move_path_to_trash(path, preclean=False)
                if move_result:
                    return True
            backoff_rmdir(path)
        if lexists(path):
            try:
                backoff_unlink(path)
                return True
            except (OSError, IOError) as e:
                log.debug("%r errno %d\nCannot unlink %s.", e, e.errno, path)
                if trash:
                    move_result = move_path_to_trash(path)
                    if move_result:
                        return True
                log.info("Failed to remove %s.", path)

        else:
            log.debug("rm_rf failed. Not a link, file, or directory: %s", path)
        return True
    finally:
        if lexists(path):
            log.info("rm_rf failed for %s", path)
            return False


def move_path_to_trash(path, preclean=True):
    """
    Move a path to the trash
    """
    from ..base.context import context
    for pkg_dir in context.pkgs_dirs:
        trash_dir = join(pkg_dir, '.trash')

        try:
            makedirs(trash_dir)
        except (IOError, OSError) as e1:
            if e1.errno != EEXIST:
                continue

        trash_file = join(trash_dir, text_type(uuid4()))

        try:
            rename(path, trash_file)
        except (IOError, OSError) as e:
            log.debug("Could not move %s to %s.\n%r", path, trash_file, e)
        else:
            log.debug("Moved to trash: %s", path)
            from ..install import delete_linked_data_any
            delete_linked_data_any(path)
            return True

    return False
