"""Kernel CI reporting I/O data"""

from inspect import stack
from warnings import warn
from kcidb_io import schema, misc # noqa Silence flake8 "imported but unused" warning


def _warn_deprecated():
    """
    Issue a warning about the calling module's function being deprecated.
    """
    func = stack()[1].function
    warn(
        f"{__name__}.{func}() is deprecated, "
        f"use {__name__}.schema.<VERSION>.{func}() instead",
        category=DeprecationWarning,
        stacklevel=3
    )


def new():
    """
    Create an empty I/O data set.

    Returns:
        An empty I/O data set adhering to the latest schema version.
    """
    _warn_deprecated()
    return schema.LATEST.new()


def count(data):
    """
    Calculate number of objects of any type in an I/O data set.

    Args:
        data:   The data set to count the objects in.

    Returns:
        The number of objects in the data set.
    """
    _warn_deprecated()
    return schema.LATEST.count(data)


def merge(target, sources, copy_target=True, copy_sources=True):
    """
    Merge multiple I/O data into a destination.

    Args:
        target:         The data to merge into.
        sources:        An iterable containing data sets to merge from.
        copy_target:    True if "target" contents should be copied before
                        upgrading and modifying. False if not.
                        Default is True.
        copy_sources:   True if "source" contents should be copied before
                        upgrading and referencing. False if not.
                        Default is True.

    Returns:
        The merged data, adhering to the latest schema version.
    """
    _warn_deprecated()
    return schema.LATEST.merge(
        target,
        sources,
        copy_target=copy_target,
        copy_sources=copy_sources
    )
